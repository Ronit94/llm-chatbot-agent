import streamlit as st
import time
import random
import os
from pymongo import MongoClient
from utils.chat_conversation import chat_session
from utils.db import add_conversation_session
from config import max_chat_history_length

# Streamed response emulator
async def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
        
def extract_text_from_pdf(file):
    return "demo"

def extract_text_from_docx(file):
    return "hello"


async def save_uploaded_file_locally(uploaded_file, folder="uploads"):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

async def streamlit_chat_interface(user_info, chat_context):
    if "chat_history" not in st.session_state:
       st.session_state.chat_history = []
    if "file_text" not in st.session_state:
       st.session_state.file_text = ""
    
    with st.sidebar:
        st.title("🤖 SQL data agent")
        st.write("Welcome to the SQL data agent! Upload your db or connection string to start querying your data.")
        st.write(f"👤 User: {user_info.get('email', 'Guest')}")
        st.write(f"🗓️ Session started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if st.button("🚪 Logout"):
            del st.session_state["user_email"]
            del st.session_state["code"]
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
        
        # if "OPENAI_API_KEY" not in os.environ:
        #     default_openai_api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") is not None else ""  # only for development environment, otherwise it should return None
        #     with st.popover("🔐 OpenAI"):
        #         openai_api_key = st.text_input(
        #             "Introduce your OpenAI API Key (https://platform.openai.com/)", 
        #             value=default_openai_api_key, 
        #             type="password",
        #             key="openai_api_key",
        #         )
        #     default_groq_api_key = os.getenv("GROQ_API_KEY") if os.getenv("GROQ_API_KEY") is not None else ""  # only for development environment, otherwise it should return None
        #     with st.popover("🔐 Groq"):
        #         groq_api_key = st.text_input(
        #             "Introduce your Groq API Key (https://console.groq.com/)", 
        #             value=default_groq_api_key, 
        #             type="password",
        #             key="groq_api_key",
        #         )
        #     default_anthropic_api_key = os.getenv("ANTROPIC_API_KEY") if os.getenv("ANTROPIC_API_KEY") is not None else "" 
        #     with st.popover("🔐 Anthropic"):
        #         anthropic_api_key = st.text_input(
        #             "Introduce your Anthropic API Key (https://console.anthropic.com/)", 
        #             value=default_anthropic_api_key,
        #             type="password",
        #             key="anthropic_api_key",
        #         )
                
        #     st.session_state["OPENAI_API_KEY"] = openai_api_key
        #     st.session_state["GROQ_API_KEY"] = groq_api_key
        #     st.session_state["ANTROPIC_API_KEY"] = anthropic_api_key
            
    st.sidebar.header("📎 Upload Document")
    uploaded_file = st.sidebar.file_uploader("Upload PDF or Word file", type=["pdf", "docx"])

    if uploaded_file:
        with st.spinner("🔄 Uploading and processing file..."):
            # Your file processing logic here
            file_path = await save_uploaded_file_locally(uploaded_file)
        st.success(f"✅ Saved file to the directory {file_path}")
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            text = ""
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            text = extract_text_from_docx(uploaded_file)
        else:
            st.sidebar.error("Unsupported file type")
            text = ""
        with st.spinner("🔪 Splitting text..."):
            raw_text = "" 
        
        print(f"Extracted text: {text}...")  # Display first 100 characters for debugging
        if raw_text:
            st.session_state.file_text = raw_text
            st.success("✅ File uploaded and processed!")
            os.remove(file_path)  # Clean up the uploaded file after processing
            
        with st.spinner("🧠 Creating embeddings and uploading to Pinecone..."):
            
            st.success("✅ Embeddings created and uploaded to Pinecone!")
    # --- Display Preview ---
    if "file_text" in st.session_state:
        print(len(chat_context))
        if len(chat_context) > max_chat_history_length:
            # st.session_state.file_text = st.session_state.file_text[:max_chat_history_length] + "..."
            st.error("you have reached the maximum chat history length, please login to a different account to continue chatting")
        
        else :# --- Chat Interface ---
            st.subheader("💬 lets ask the bot now")
            user_input = st.chat_input("Type your question here")
            session_id = user_info.get("sub", "session_123")
            if user_input:
                # 🔁 Simple mock response (replace with real LLM logic)
                llm_response = chat_session(session_id= session_id,
                            input_text=user_input,
                            user_info={"email": user_info.get("email", "Guest")})
                
                if llm_response:
                    response = llm_response.get("response", "Sorry, I couldn't process your request.")

                # Append to chat history
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                    
                st.session_state.chat_history.append(("user", user_input))
                st.session_state.chat_history.append(("bot", response))
                
                obj = {"question": user_input, "answer": response}
                
                add_conversation_session(email=user_info.get("email", "Guest"), chat_context=obj)

        # --- Display Chat ---
        if "chat_history" in st.session_state:
            for role, msg in st.session_state.chat_history:
                with st.chat_message(role):
                    st.markdown(msg)
    else:
        st.info("⬅️ Upload a file to begin.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
