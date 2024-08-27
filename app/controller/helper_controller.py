import logging
import streamlit as st
from app.model.files_model import save_image_to_folder, clear_saved_images
from app.model.chat_history_model import clear_chat_history, clear_saved_chat_histories, save_chat_history
import os

def handle_image_saving(image_path):
    logging.info("Saving image to folder.")
    if not image_path:
        logging.error("No image to save.")
        return

    save_path = save_image_to_folder(image_path)

    if "saved_images" not in st.session_state:
        st.session_state.saved_images = []
    st.session_state.saved_images.append(save_path)
    logging.info(f"Image saved to folder: {save_path}")


def handle_clear_saved_images():
    logging.info("Clearing saved images.")
    clear_saved_images()
    st.session_state.saved_images = []
    logging.info("Saved images cleared.")


def handle_clear_chat_history():
    logging.info("Handling request to clear chat history.")
    clear_chat_history()

def handle_save_chat_history():
    logging.info("Handling request to save chat history.")
    save_chat_history()

def handle_clear_saved_chat_histories():
    logging.info("Handling request to clear saved chat histories.")
    clear_saved_chat_histories()


def handle_saved_posts():
    if "saved_posts" in st.session_state:
        st.session_state.saved_posts = [post for post in st.session_state.saved_posts if os.path.exists(post["image_path"])]
    
    return st.session_state.get("saved_posts", [])