import logging
import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def generate_image(prompt):
    """
    Generates an image from the given prompt using an API.

    Args:
        prompt (str): The text prompt for image generation.

    Returns:
        str: The file path of the generated image, or None if generation fails.
    """
    print(f"Generating image with prompt: {prompt}")
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "jpeg",
        },
    )
    if response.status_code == 200:
        file_path = f"./generated_image_{len(st.session_state.generated_images)}.jpeg"
        with open(file_path, 'wb') as file:
            file.write(response.content)
        st.session_state.generated_images.append(file_path)
        return file_path  # Ensure that the returned value is a string
    else:
        error_message = str(response.json())
        print(f"Image generation failed: {error_message}")
        return None


    
def modify_image(previous_image_path, modification_prompt):
    print(f"Modifying image {previous_image_path} with prompt: {modification_prompt}")

    try:
        with open(previous_image_path, 'rb') as image_file:
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/edit/search-and-replace",  
                headers={
                    "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",  
                    "Accept": "image/*"
                },
                files={"image": image_file},
                data={
                    "search_prompt": modification_prompt,
                    "prompt": modification_prompt
                }
            )

        if response.status_code == 200:
            modified_image_path = f"./modified_image_{len(st.session_state.generated_images)}.jpeg"
            with open(modified_image_path, 'wb') as file:
                file.write(response.content)
            st.session_state.generated_images.append(modified_image_path)
            return modified_image_path
        else:
            print(f"Image modification failed: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred during image modification: {e}")
        return None
    
def remove_background(previous_image_path):
    print(f"Removing background from image: {previous_image_path}")

    try:
        with open(previous_image_path, 'rb') as image_file:
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/edit/remove-background",
                headers={
                    "authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",  
                    "accept": "image/*"
                },
                files={"image": image_file},
                data={"output_format": "webp"}
            )

        if response.status_code == 200:
            modified_image_path = f"./background_removed_{len(st.session_state.generated_images)}.webp"
            with open(modified_image_path, 'wb') as file:
                file.write(response.content)
            st.session_state.generated_images.append(modified_image_path)
            return modified_image_path
        else:
            print(f"Background removal failed: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred during background removal: {e}")
        return None


def outpaint_image(previous_image_path, left, right, up, down):
    print(f"Outpainting image {previous_image_path} with parameters - Left: {left}, Right: {right}, Up: {up}, Down: {down}")

    try:
        with open(previous_image_path, 'rb') as image_file:
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/edit/outpaint",
                headers={
                    "authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
                    "accept": "image/*"
                },
                files={"image": image_file},
                data={
                    "left": left,
                    "right": right,
                    "up": up,
                    "down": down,
                    "output_format": "webp"
                }
            )

        if response.status_code == 200:
            outpainted_image_path = f"./outpainted_image_{len(st.session_state.generated_images)}.webp"
            with open(outpainted_image_path, 'wb') as file:
                file.write(response.content)
            st.session_state.generated_images.append(outpainted_image_path)
            return outpainted_image_path
        else:
            print(f"Outpainting failed: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred during outpainting: {e}")
        return None