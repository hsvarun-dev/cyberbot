import os
import subprocess
from flask import Flask, request, jsonify  # Ensure Flask components are properly imported

# File to store admin credentials
ADMIN_CREDENTIALS_FILE = "admin_credentials.txt"

def setup_admin_credentials():
    """Stores admin credentials and prevents modifications"""
    if not os.path.exists(ADMIN_CREDENTIALS_FILE):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        with open(ADMIN_CREDENTIALS_FILE, "w") as file:
            file.write(f"{username}:{password}")

        print("✅ Admin credentials saved successfully! 🚀")
    else:
        print("⚠ Admin credentials already exist and cannot be changed.")

# Run admin credential setup before starting the Flask app
setup_admin_credentials()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Security Bot Running on Python Flask!"

# Function to execute PowerShell scripts with pop-up & logs
def run_powershell(script_path):
    try:
        # Open PowerShell visibly for real-time execution
        subprocess.run(
            ["powershell.exe", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", script_path],
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Opens in a separate PowerShell window
        )

        # Capture terminal output for UI streaming
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

@app.route('/bot', methods=['POST'])
def bot():
    request_data = request.get_json()

    # Read stored admin credentials
    with open(ADMIN_CREDENTIALS_FILE, "r") as file:
        stored_credentials = file.read().strip().split(":")
    
    admin_user = stored_credentials[0]
    admin_pass = stored_credentials[1]

    # Verify credentials - Exit early if incorrect
    if request_data.get("username") != admin_user or request_data.get("password") != admin_pass:
        return jsonify({"status": "error", "logs": "❌ Authentication failed! Invalid admin credentials."})

    # Proceed only if authentication is successful
    command = request_data.get("message", "").strip().lower()

    # Define security-related PowerShell script paths
    scripts = {
        "check system status": "scripts/checkSystemStatus.ps1",
        "update antivirus": "scripts/updateAntivirus.ps1",
        "scan vulnerabilities": "scripts/scanVulnerabilities.ps1",
        "install patches": "scripts/installSecurityPatch.ps1",
        "monitor logs": "scripts/monitorLogs.ps1"
    }

    response = run_powershell(scripts.get(command, None)) if command in scripts else {
        "status": "unknown",
        "logs": "🤖 Invalid command! Try 'install patches', 'monitor logs', 'update antivirus', 'scan vulnerabilities', or 'check system status'."
    }
    return jsonify(response)

if __name__ == '__main__':
    print("✅ Security Bot is starting on port 3978...")
    app.run(port=3978, debug=True)  # Debug mode enabled for easier troubleshooting