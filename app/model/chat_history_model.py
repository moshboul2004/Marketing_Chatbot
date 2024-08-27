import logging
from langchain_core.messages import HumanMessage
import streamlit as st


from dotenv import load_dotenv

load_dotenv()


def clear_chat_history():
    if "chat_initialized" in st.session_state:
        del st.session_state.chat_history
        del st.session_state.chat_initialized
    logging.info("Chat history cleared.")

def save_chat_history():
    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        st.error("Chat history is empty. Nothing to save.")
        return

    if "saved_chats" not in st.session_state:
        st.session_state.saved_chats = []

    readable_chat = []
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            readable_chat.append(f"User: {message.content}")
        else:
            readable_chat.append(f"Assistant: {message.content}")

    st.session_state.saved_chats.append("\n".join(readable_chat))
    logging.info("Chat history saved.")
    st.success("Chat history saved successfully.")

def clear_saved_chat_histories():
    if "saved_chats" in st.session_state:
        del st.session_state.saved_chats
    logging.info("Saved chat histories cleared.")

