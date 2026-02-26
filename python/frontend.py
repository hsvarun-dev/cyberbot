import streamlit as st
import requests
import os

# API URL (Server Backend)
BASE_URL = "http://127.0.0.1:3978/bot"

st.set_page_config(page_title="Security Bot Interface", page_icon="🔐", layout="centered")

# Styling UI
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0f4f8 100%);
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        min-height: 350px;
        margin-bottom: 20px;
        background: rgba(236, 239, 255, 0.6);
        border-radius: 18px;
        padding: 24px 16px;
        box-shadow: 0 2px 16px rgba(99, 102, 241, 0.08);
    }
    .stTextInput>div>div>input {
        border-radius: 18px;
        border: 1.5px solid black;
        background: black;
        padding: 10px 16px;
        font-size: 1.1em;
    }
    .stButton>button {
        border-radius: 18px;
        background: linear-gradient(90deg, black 60%, black 100%);
        color: white;
        font-weight: bold;
        font-size: 1.1em;
        padding: 8px 28px;
        border: none;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.12);
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, black 60%, black 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Page Header
st.title("🔐 Security Bot Interface")

# User Inputs
username = st.text_input("Admin Username:")
password = st.text_input("Admin Password:", type="password")
command = st.text_input("Enter security command:")

# Button to Run Command
if st.button("Execute"):
    if username and password and command:
        # Prepare JSON request
        data = {"username": username, "password": password, "message": command}
        
        # Send request to backend API
        response = requests.post(BASE_URL, json=data)
        result = response.json()

        # Display Logs in Streamlit UI
        st.write("### 📝 Command Output:")
        st.code(result["logs"], language="powershell")  # Formats logs for better readability

        # Show execution status
        if result["status"] == "success":
            st.success("✅ Execution Successful!")
        else:
            st.error("❌ Execution Failed!")

    else:
        st.warning("⚠ Please enter all fields (Command, Username, Password)!")

st.markdown("---")
st.caption("Made with Streamlit • Secure Security Bot UI")