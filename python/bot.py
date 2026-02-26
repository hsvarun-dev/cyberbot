from flask import Flask, request, jsonify
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_PORT = int(os.getenv("BOT_PORT", "3978"))  # Defaults to 3978 if BOT_PORT is not set
ADMIN_CREDENTIALS_FILE = "admin_credentials.txt"

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Security Bot Running on Python Flask!"

# Function to run PowerShell scripts with UI + Terminal Output
def run_powershell(script_path):
    try:
        # Open PowerShell window visibly
        subprocess.run(["powershell.exe", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", script_path], shell=True)

        # Capture output for UI streaming
        process = subprocess.Popen(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        stdout, stderr = process.communicate()

        return {
            "status": "success" if process.returncode == 0 else "error",
            "logs": stdout.decode().strip() if stdout else stderr.decode().strip()
        }
    except Exception as e:
        return {"status": "error", "logs": str(e)}

# Function to verify admin credentials before executing commands
def authenticate_admin(username, password):
    if not os.path.exists(ADMIN_CREDENTIALS_FILE):
        return False

    with open(ADMIN_CREDENTIALS_FILE, "r") as file:
        stored_credentials = file.read().strip().split(":")
    
    return username == stored_credentials[0] and password == stored_credentials[1]

# API endpoint for security operations
@app.route('/bot', methods=['POST'])
def security_bot():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    command = data.get("message", "").lower()

    # Authenticate admin before executing any command
    if not authenticate_admin(username, password):
        return jsonify({"status": "error", "logs": "❌ Authentication failed! Invalid admin credentials."})

    # Define security-related PowerShell script paths
    scripts = {
        "install patches": "scripts/installSecurityPatch.ps1",
        "monitor logs": "scripts/monitorLogs.ps1",
        "update antivirus": "scripts/updateAntivirus.ps1",
        "scan vulnerabilities": "scripts/scanVulnerabilities.ps1",
        "check domain servers": "scripts/checkDomainServers.ps1"
    }

    response = run_powershell(scripts.get(command, None)) if command in scripts else {
        "status": "unknown",
        "message": "🤖 Try 'install patches', 'monitor logs', 'update antivirus', 'scan vulnerabilities', or 'check domain servers'."
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=BOT_PORT, debug=True)  # Debug mode enabled for easier troubleshooting