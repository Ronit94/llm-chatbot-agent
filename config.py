import streamlit as st

google_client_id = st.secrets["GOOGLE_CLIENT_ID"]
google_client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
redirect_url = st.secrets["REDIRECT_URI"]
token_url = st.secrets["TOKEN_URL"]
auth_url = st.secrets["AUTH_URL"]
user_info_url = st.secrets["USER_INFO_URL"]
database_url = st.secrets["DATABASE_URL"]
pin_cone_api_key = st.secrets["PINCONE_API_KEY"]
index_name = st.secrets["PINECONE_INDEX_NAME"]
anthropic_api_key = st.secrets["ANTROPIC_API_KEY"]
dba_server_base_url = st.secrets["DBA_SERVER_BASE_URL"]
max_chat_history_length = st.secrets["MAX_CHAT_HISTORY_LENGTH"]
# Google OAuth 2.0 configuration

