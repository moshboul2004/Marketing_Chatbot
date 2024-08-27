import logging
import streamlit as st
from app.model.files_model import save_post

def handle_save_post():
    if "saved_images" in st.session_state and st.session_state.saved_images:
        last_image_path = st.session_state.saved_images[-1]
        logging.info(f"Last image path: {last_image_path}")
    else:
        st.error("No images available to save as caption.")
        return

    if "chat_history" in st.session_state and st.session_state.chat_history:
        last_assistant_response = st.session_state.chat_history[-1].content
        logging.info(f"Last assistant response: {last_assistant_response}")
    else:
        st.error("No text available to save as a caption.")
        return

    post = save_post(last_image_path, last_assistant_response)
    if post:
        st.success("Post saved successfully!")
        logging.info("Post saved successfully")
    else:
        st.error("Failed to save the post.")
        logging.error("Failed to save the post.")

