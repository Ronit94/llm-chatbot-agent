import requests
from config import dba_server_base_url


def chat_session(session_id, input_text, user_info):
    print(session_id)
    url = f"{dba_server_base_url}/conversations/chat/start"
    response = requests.post(url, json={
        "session_id": session_id,
        "input": input_text})
    if response.status_code == 200:
        print("Session saved successfully.")
        return response.json()
    else:
        print(f"Error saving session: {response.status_code} - {response.text}")