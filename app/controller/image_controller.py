import logging
import streamlit as st
from app.model.image_model import generate_image, modify_image, remove_background, outpaint_image
from app.model.files_model import save_image_to_folder
import os



def handle_image_generation(prompt):
    logging.info("Handling image generation session.")

    file_path = generate_image(prompt)
    if file_path:
        logging.info(f"Image generated successfully: {file_path}")
        
        if "saved_images" not in st.session_state:
            st.session_state.saved_images = []
        st.session_state.saved_images.append(file_path)

        st.session_state.saved_images[-1] = file_path
        logging.info(f"Updated saved images with the new image: {file_path}")

        return file_path
    else:
        logging.error("Image generation failed. Please try again.")
        return None



def handle_image_modification(previous_image_path, modification_prompt):
    logging.info("Handling image modification session.")

    if "generated_images" not in st.session_state or not st.session_state.generated_images:
        st.error("No images available to modify.")
        return None

    file_path = modify_image(previous_image_path, modification_prompt)
    if file_path:
        logging.info(f"Image modified successfully: {file_path}")
        save_path = save_image_to_folder(file_path)
        logging.info(f"Image saved to folder: {save_path}")
        return save_path
    else:
        logging.error("Image modification failed. Please try again.")
        return None
    


def handle_background_removal(previous_image_path):
    logging.info("Handling background removal session.")

    if "generated_images" not in st.session_state or not st.session_state.generated_images:
        st.error("No images available to modify.")
        return None

    file_path = remove_background(previous_image_path)
    if file_path:
        logging.info(f"Background removed successfully: {file_path}")
        save_path = save_image_to_folder(file_path)
        logging.info(f"Image saved to folder: {save_path}")
        return save_path
    else:
        logging.error("Background removal failed. Please try again.")
        return None



def handle_outpainting(previous_image_path, left, right, up, down):
    logging.info("Handling outpainting session.")

    if "generated_images" not in st.session_state or not st.session_state.generated_images:
        st.error("No images available to outpaint.")
        return None

    file_path = outpaint_image(previous_image_path, left, right, up, down)
    if file_path:
        logging.info(f"Image outpainted successfully: {file_path}")
        save_path = save_image_to_folder(file_path)
        logging.info(f"Image saved to folder: {save_path}")
        return save_path
    else:
        logging.error("Outpainting failed. Please try again.")
        return None



