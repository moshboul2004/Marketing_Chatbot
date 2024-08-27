import logging
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st
from streamlit_chat import message
from app.model.serpapi_model import fetch_google_search,fetch_google_trends,fetch_local_results, spell_check


def handle_google_search(query):
    logging.info(f"Handling analytics query: {query}")

    search = fetch_google_search(query)
    
    logging.info(f"Google Search results: {search}")
    return search

def handle_google_trends(query):
    logging.info(f"Handling analytics query: {query}")
    
    trends = fetch_google_trends(query)

    logging.info(f"Google Trend results: {trends}")
    return trends


def handle_local_api_chat():
    logging.info("Handling chat session in Local mode.")

    if "chat_initialized" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_initialized = True
        logging.info("Chat history reset.")

    logging.info("Accessing chat history.")
    for i, message_data in enumerate(st.session_state.chat_history):
        if isinstance(message_data, HumanMessage):
            message(message_data.content, is_user=True, avatar_style="miniavs", key=f"user_{i}")
            logging.info(f"Displayed human message: {message_data.content}")
        else:
            message(message_data.content, avatar_style="bottts", key=f"ai_{i}")
            logging.info(f"Displayed AI message: {message_data.content}")

    user_query = st.chat_input('Your message')
    
    if user_query is not None and user_query != "":
        logging.info(f"User input received: {user_query}")
        
        corrected_query = spell_check(user_query)
        logging.info(f"User input after spell check: {corrected_query}")

        message(corrected_query, is_user=True, avatar_style="miniavs", key=f"user_input_{len(st.session_state.chat_history)}")
        logging.info(f"Displayed corrected user input: {corrected_query}")

        logging.info("Generating AI response in Local mode.")
        
        ai_response_content = fetch_local_results(corrected_query)
        
        message(ai_response_content, avatar_style="bottts", key=f"ai_response_{len(st.session_state.chat_history)}")
        logging.info(f"AI response generated: {ai_response_content}")

        user_message = HumanMessage(corrected_query)
        ai_response = AIMessage(ai_response_content)

        logging.info("Updating chat history with user message.")
        st.session_state.chat_history.append(user_message)
        logging.info("User message appended to chat history.")

        logging.info("Updating chat history with AI response.")
        st.session_state.chat_history.append(ai_response)
        logging.info("AI response appended to chat history.")

def handle_mode_switch(selected_mode):
    if "previous_mode" not in st.session_state:
        st.session_state.previous_mode = selected_mode
    
    if st.session_state.previous_mode != selected_mode:
        if st.session_state.previous_mode == "Chatbot":
            st.session_state.chatbot_history = st.session_state.chat_history
        elif st.session_state.previous_mode == "Local":
            st.session_state.local_history = st.session_state.chat_history
        
        st.session_state.chat_history = []
        
        if selected_mode == "Chatbot":
            st.session_state.chat_history = st.session_state.get("chatbot_history", [])
        elif selected_mode == "Local":
            st.session_state.chat_history = st.session_state.get("local_history", [])
        
        st.session_state.previous_mode = selected_mode
