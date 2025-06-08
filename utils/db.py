from pymongo import MongoClient
from config import database_url, dba_server_base_url
import requests
# --- Setup MongoDB ---



def save_session(email, token, user_info):
    print(email)
    url = f"{dba_server_base_url}/db/save-session"
    response = requests.post(url, json={
        "email": email,
        "token": token,
        "user_info": user_info})
    if response.status_code == 200:
        print("Session saved successfully.")
    else:
        print(f"Error saving session: {response.status_code} - {response.text}")
    

def add_conversation_session(email, chat_context):
    url = f"{dba_server_base_url}/db/add-conversation-session"
    response = requests.post(url, json={
        "email": email,
        "chat_context": chat_context})
    if response.status_code == 200:
        print("Conversation session added successfully.")
    else:
        print(f"Error adding conversation session: {response.status_code} - {response.text}")    
        


def get_saved_session(email):
    url = f"{dba_server_base_url}/db/get-session/{email}"
    session = requests.get(url)
    if session.status_code == 200:
        session_data = session.json()
        if session_data and "data" in session_data:
            return session_data.get("data", None)
    else:
        print(f"Error fetching session: {session.status_code} - {session.text}")
        return None
    
    