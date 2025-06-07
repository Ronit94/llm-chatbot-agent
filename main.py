import streamlit as st
import logging
import os
from pymongo import MongoClient
import asyncio
from authlib.integrations.requests_client import OAuth2Session
from config import redirect_url, google_client_id, google_client_secret, auth_url, token_url, user_info_url
import time
from rich.console import Console
from design.chatbot import streamlit_chat_interface
from utils.db import save_session, get_saved_session



os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="app.log",  # or omit this line to log to console
    filemode="a"
)


client = OAuth2Session(
    client_id=google_client_id,
    client_secret=google_client_secret,
    redirect_uri=redirect_url,
    scope="openid email profile"
)


st.set_page_config(page_title="🤖 SQL data agent", layout="centered")
st.title("🤖 SQL data agent")





async def main():
    print("Streamlit app started successfully")
    if "user_email" in st.session_state:
        saved = get_saved_session(st.session_state["user_email"])
        if saved and time.time() < saved["expires_at"]:
            user_info = saved["user_info"]
            await streamlit_chat_interface(user_info)
        else:
            st.warning("Session expired. Please log in again.")
            del st.session_state["user_email"]
            st.rerun()
    else:
        # Check OAuth redirect
        # query_params = st.experimental_get_query_params()
        query_params = st.query_params
        # code = query_params.get("code", [None])[0]
        code = query_params.get("code", None)

        print("code==================>", code)
        st.session_state["code"] = code

        if code and "token" not in st.session_state:
            # Exchange code for token
            token = client.fetch_token(
                token_url,
                code=code
            )
            token["expires_at"] = time.time() + token.get("expires_in", 3600)
            client.token = token
            user_info = client.get(user_info_url).json()

            # Save session to MongoDB
            save_session(user_info["email"], token, user_info)

            # Set session
            st.session_state["user_email"] = user_info["email"]
            st.session_state["token"] = token
            st.rerun()

        else:
            # No session yet — show login
            auth_url2, _ = client.create_authorization_url(auth_url)
            st.markdown("Login using your Google Account:")
            if st.button("🔑 Login with Google"):
                # Redirect to Google OAuth
                print("Redirecting to Google OAuth...")
                st.markdown(f"<meta http-equiv='refresh' content='0; url={auth_url2}'>", unsafe_allow_html=True)
               
        

if __name__ == "__main__":
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error starting Streamlit app: {e}")
        st.error("An error occurred while starting the app. Please check the logs for more details.")