import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_PORT = int(os.getenv("BOT_PORT", "3978"))  # Defaults to 3978 if BOT_PORT is not set
BASE_URL = f"http://127.0.0.1:{BOT_PORT}/bot"

# File to store admin credentials
ADMIN_CREDENTIALS_FILE = "admin_credentials.txt"

def get_admin_credentials():
    """Retrieve stored admin credentials"""
    if not os.path.exists(ADMIN_CREDENTIALS_FILE):
        print("❌ Admin credentials not found! Set up credentials first.")
        return None, None

    with open(ADMIN_CREDENTIALS_FILE, "r") as file:
        stored_credentials = file.read().strip().split(":")
    
    return stored_credentials[0], stored_credentials[1]  # Returns admin username and password

# Function to send API requests with authentication
def send_request(message):
    """Send API request to bot with credentials"""
    admin_user, admin_pass = get_admin_credentials()

    if not admin_user or not admin_pass:
        print("❌ Cannot proceed without valid admin credentials.")
        return {"status": "error", "logs": "Authentication required."}

    data = {
        "username": admin_user,
        "password": admin_pass,
        "message": message
    }

    response = requests.post(BASE_URL, json=data)
    return response.json()

# Test security automation tasks and display logs
test_commands = [
    "install patches",
    "monitor logs",
    "update antivirus",
    "scan vulnerabilities",
    "check domain servers"
]

print("\n🔐 Running Security Tests...\n")

for command in test_commands:
    result = send_request(command)
    
    print(f"🛠 **Command:** {command}")
    print(f"✅ **Status:** {result.get('status', 'Unknown')}")
    print(f"📜 **Logs:**\n{result.get('logs', 'No logs available')}")
    print("-" * 50)