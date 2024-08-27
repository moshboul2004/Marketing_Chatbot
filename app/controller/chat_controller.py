import logging
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st
from streamlit_chat import message
from app.model.chat_model import get_response
from app.model.serpapi_model import spell_check



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])

logging.info("Chat controller initialized.")

# def handle_chat():
#     logging.info("Handling chat session.")

#     if "chat_initialized" not in st.session_state:
#         st.session_state.chat_history = []
#         st.session_state.chat_initialized = True
#         logging.info("Chat history reset.")

#     logging.info("Accessing chat history.")
#     for i, message_data in enumerate(st.session_state.chat_history):
#         if isinstance(message_data, HumanMessage):
#             message(message_data.content, is_user=True, avatar_style="miniavs", key=f"user_{i}")
#             logging.info(f"Displayed human message: {message_data.content}")
#         else:
#             message(message_data.content, avatar_style="bottts", key=f"ai_{i}")
#             logging.info(f"Displayed AI message: {message_data.content}")

#     user_query = st.chat_input('Your message')
    
#     if user_query is not None and user_query != "":
#         user_message = HumanMessage(user_query)
#         logging.info(f"User input received: {user_query}")

#         message(user_query, is_user=True, avatar_style="miniavs", key=f"user_input_{len(st.session_state.chat_history)}")
#         logging.info(f"Displayed user input: {user_query}")

#         logging.info("Generating AI response.")
#         ai_response_content = get_response(st.session_state.username, user_query, st.session_state.chat_history)
        
#         message(ai_response_content, avatar_style="bottts", key=f"ai_response_{len(st.session_state.chat_history)}")
#         logging.info(f"AI response generated: {ai_response_content}")

#         ai_response = AIMessage(ai_response_content)

#         logging.info("Updating chat history with user message.")
#         st.session_state.chat_history.append(user_message)
#         logging.info("User message appended to chat history.")

#         logging.info("Updating chat history with AI response.")
#         st.session_state.chat_history.append(ai_response)
#         logging.info("AI response appended to chat history.")





# Function with spelling check and local API


def handle_chat():
    logging.info("Handling chat session.")

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

        logging.info("Generating AI response.")
        
        ai_response_content = get_response(st.session_state.username, corrected_query, st.session_state.chat_history)
        
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


