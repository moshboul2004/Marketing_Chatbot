import logging
import streamlit as st
import os



def save_image_to_folder(image_path):
    if not os.path.exists("saved_images"):
        os.makedirs("saved_images")
    
    image_name = os.path.basename(image_path)
    save_path = os.path.join("saved_images", image_name)
    with open(save_path, 'wb') as f:
        f.write(open(image_path, 'rb').read())

    if "saved_images" not in st.session_state:
        st.session_state.saved_images = []
    
    st.session_state.saved_images.append(save_path)
    return save_path


def clear_saved_images():
    if "saved_images" in st.session_state:
        for file_path in st.session_state.saved_images:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logging.info(f"Removed file: {file_path}")
            except Exception as e:
                logging.error(f"Error removing file {file_path}: {e}")
        st.session_state.saved_images = []

    if os.path.exists("saved_images"):
        for file in os.listdir("saved_images"):
            file_path = os.path.join("saved_images", file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"Removed file from folder: {file_path}")
            except Exception as e:
                logging.error(f"Error removing file from folder {file_path}: {e}")
        os.rmdir("saved_images")
        logging.info("Removed 'saved_images' directory")


def save_post(image_path, caption):
    if not os.path.exists("saved_posts"):
        os.makedirs("saved_posts")
    
    post_data = {
        "image_path": image_path,
        "caption": caption
    }
    
    if "saved_posts" not in st.session_state:
        st.session_state.saved_posts = []
    
    st.session_state.saved_posts.append(post_data)
    return post_data

