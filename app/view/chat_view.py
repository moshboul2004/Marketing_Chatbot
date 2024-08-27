import os
import streamlit as st
import logging
from app.controller.chat_controller import handle_chat
from app.controller.image_controller import handle_image_generation, handle_background_removal, handle_image_modification, handle_outpainting
from app.controller.serpapi_controller import handle_google_search, handle_google_trends, handle_local_api_chat, handle_mode_switch
from app.controller.helper_controller import handle_clear_saved_images, handle_image_saving, handle_clear_chat_history, handle_clear_saved_chat_histories, handle_save_chat_history, handle_saved_posts
from app.controller.auth_controller import handle_log_in, handle_sign_up
from app.controller.canvas_contrller import handle_canvas
from app.controller.editor_controller import handle_cropper
from app.controller.calendar_controller import handle_calendar
from app.controller.post_controller import handle_save_post
from app.controller.analytics_controller import handle_analytics
from app.util.pdf_generator import generate_pdf, generate_pdf_with_caption
from app.util.get_time_date import get_current_date_and_time
from app.util.database import initialize_db

import cv2

logging.info("Setting up the Streamlit interface.")


def setup_interface():
    initialize_db()
    st.set_page_config(page_title="Marketing Assistant")

    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
        }
        .form-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .form-field {
            margin-bottom: 20px;
        }
        .toggle-switch {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown('<h1 class="centered-title">Welcome to the Marketing Assistant</h1>', unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
            <style>
            /* Add padding to the selectbox */
            .stSelectbox {
                padding: 30px 0px;
            }
            </style>
        """, unsafe_allow_html=True)

        form_type = st.selectbox("Select Login or Sign Up", ["Login", "Sign Up"], index=0, key="form_type")
        
        with st.container():
            if form_type == "Login":
                st.markdown('<h2 class="centered-title">Login</h2>', unsafe_allow_html=True)
                username = st.text_input("Username", key="login_username", placeholder="Enter your username", help="Enter your registered username")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password", help="Enter your password")

                if st.button("Login"):
                    if handle_log_in(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

            elif form_type == "Sign Up":
                st.markdown('<h2 class="centered-title">Sign Up</h2>', unsafe_allow_html=True)
                username = st.text_input("Username", key="signup_username", placeholder="Choose a username", help="Enter a unique username")
                password = st.text_input("Password", type="password", key="signup_password", placeholder="Choose a password", help="Enter a secure password")

                if st.button("Sign Up"):
                    if handle_sign_up(username, password):
                        st.success("Sign up successful! Please log in.")
                    else:
                        st.error("Username already exists.")
            st.markdown('</div>', unsafe_allow_html=True)

        return  

    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
        }
        .h2-no-padding {
            font-size: 1.5em;
            font-weight: bold;
            margin: 0 0 0 0; 
            padding: 0; 
        }
        .centered-inline-text {
            text-align: center;
            margin: 0; 
            padding: 0;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    date, time = get_current_date_and_time()
    st.sidebar.markdown('<h1 class="centered-title">Marketing Assistant</h1>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<p class="centered-inline-text">Logged in as: {st.session_state.username}</div>', unsafe_allow_html=True)


    st.sidebar.markdown("---")
    st.sidebar.markdown(f'<p class="centered-inline-text">{time} | {date}</p>', unsafe_allow_html=True)

    st.sidebar.markdown("---")

    with st.sidebar:
        mode = st.sidebar.radio("#### Select Mode", ["Chatbot", "Image Generator","Social Media","Analytics", "Trends","Editor", "Canvas", "Calendar"], index=0)        
        st.sidebar.markdown("---")

        st.markdown("Chatbot Actions")
        st.button("🗑️ Clear history", help="Clear history", on_click=handle_clear_chat_history)
        st.button("💾 Save chat history", help="Save history", on_click=handle_save_chat_history)
        st.sidebar.markdown("---")

        if "saved_chats" in st.session_state or ("saved_images" in st.session_state and st.session_state.saved_images):
            st.sidebar.markdown("Saved")



            if "saved_chats" in st.session_state:
                with st.sidebar.expander("💬 Saved Chat Histories", expanded=False):
                    for i, chat in enumerate(st.session_state.saved_chats):
                        st.markdown(f"### Chat History {i+1}")
                        st.text_area(label=f"Chat History {i+1}", value=chat, height=200, key=f"saved_chat_{i}")
                        pdf = generate_pdf(chat)
                        st.download_button(label="📥 Download as PDF", data=pdf, file_name=f"chat_history_{i+1}.pdf", mime="application/pdf")
                    st.button("🗑️ Clear saved history", help="Clear saved history", on_click=handle_clear_saved_chat_histories)

        

            if "saved_images" in st.session_state and st.session_state.saved_images:
                    with st.sidebar.expander("🖼️ Saved Images", expanded=False):
                        for i, image_path in enumerate(st.session_state.saved_images):
                            st.image(image_path, caption=f"Saved Image {i+1}")
                            st.download_button(label="📥 Download Image", data=open(image_path, 'rb').read(), file_name=f"saved_image_{i+1}.jpeg", mime="image/jpeg")
                        st.button("🗑️ Clear saved images", help="Clear saved images", on_click=handle_clear_saved_images)





    if mode == "Chatbot":
        st.markdown('<h1 style="text-align: center;">Chatbot Mode</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        chat_model = st.selectbox("Select model type", ["Chatbot", "Local Chatbot"])
        handle_mode_switch(chat_model)
        
        
        if chat_model == "Chatbot":
            handle_chat()  
        
        elif chat_model == "Local Chatbot":
            handle_local_api_chat()  
                
        if st.button("💾 Save Caption"):
            handle_save_post()  



  

    elif mode == "Image Generator":
        st.markdown('<h1 style="text-align: center;">Image Generator Mode</h1>', unsafe_allow_html=True)
        st.markdown("---")

        image_model = st.selectbox("Select model type", ["Text-to-Image", "Search and Replace", "Remove Background", "Outpaint"], index=0)
        
        if "generated_images" not in st.session_state:
            st.session_state.generated_images = []

        if image_model == "Text-to-Image":
            prompt = st.chat_input('Enter the prompt for image generation')
            if prompt:
                with st.spinner('Generating image...'):
                    file_path = handle_image_generation(prompt)
                if file_path:
                    st.image(file_path, caption="Generated Image")
                    if st.button("💾 Save"):
                        handle_image_saving(file_path, image_type="generated")
                      
                else:
                    st.error("Image generation failed. Please try again.")


        elif image_model == "Search and Replace":
            uploaded_file = st.file_uploader("Upload an image to modify", type=["jpeg", "png"])
            modification_prompt = st.chat_input('Enter the prompt for modification')
            
            if uploaded_file:
                previous_image_path = f"./uploaded_{len(st.session_state.generated_images)}.jpeg"
                with open(previous_image_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())
                st.session_state.generated_images.append(previous_image_path)
                st.image(previous_image_path, caption=f"Uploaded Image ({uploaded_file.name})")

            if modification_prompt and uploaded_file:
                with st.spinner('Modifying image...'):
                    modified_image_path = handle_image_modification(previous_image_path, modification_prompt)
                if modified_image_path:
                    st.image(modified_image_path, caption="Modified Image")
                    if st.button("💾 Save"):
                        handle_image_saving(modified_image_path, image_type="modified")
                else:
                    st.error("Image modification failed. Please try again.")


        elif image_model == "Remove Background":
            uploaded_file = st.file_uploader("Upload an image to remove background", type=["jpeg", "png"])
            if uploaded_file:
                previous_image_path = f"./uploaded_{len(st.session_state.generated_images)}.jpeg"
                with open(previous_image_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())
                st.session_state.generated_images.append(previous_image_path)
                st.image(previous_image_path, caption=f"Uploaded Image ({uploaded_file.name})")

                if st.button("Remove Background"):
                    with st.spinner('Removing background...'):
                        background_removed_image_path = handle_background_removal(previous_image_path)
                    if background_removed_image_path:
                        st.image(background_removed_image_path, caption="Background Removed")
                        if st.button("💾 Save image with background removed"):
                            handle_image_saving(background_removed_image_path, image_type="modified")
                    else:
                        st.error("Background removal failed. Please try again.")
        

        elif image_model == "Outpaint":
            uploaded_file = st.file_uploader("Upload an image to outpaint", type=["jpeg", "png"])
            if uploaded_file:
                previous_image_path = f"./uploaded_{len(st.session_state.generated_images)}.jpeg"
                with open(previous_image_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())
                st.session_state.generated_images.append(previous_image_path)
                st.image(previous_image_path, caption=f"Uploaded Image ({uploaded_file.name})")

                left = st.number_input("Left:", min_value=0)
                right = st.number_input("Right:", min_value=0)
                up = st.number_input("Up:", min_value=0)
                down = st.number_input("Down:", min_value=0)

                if st.button("Outpaint"):
                    with st.spinner('Outpainting image...'):
                        outpainted_image_path = handle_outpainting(previous_image_path, left, right, up, down)
                    if outpainted_image_path:
                        st.image(outpainted_image_path, caption="Outpainted Image")
                        if st.button("💾 Save"):
                            handle_image_saving(outpainted_image_path, image_type="modified")
                    else:
                        st.error("Outpainting failed. Please try again.")
    if mode == "Social Media":
        st.markdown('<h1 style="text-align: center;">Social Media Mode</h1>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Posts")

        saved_posts = handle_saved_posts()
        if saved_posts:
            for post in saved_posts:
                st.image(post['image_path'], caption=post['caption'])
                st.markdown("---")

            pdf_buffer = generate_pdf_with_caption(saved_posts)
            st.download_button(
                label="📥 Download Posts",
                data=pdf_buffer,
                file_name="social_media_posts.pdf",
                mime="application/pdf"
            )
        else:
            st.info("No posts available.")
        if st.button("Schedule a Post"):
            st.warning("Not implemented")
        if st.button("Post"):
            st.warning("Not implemented")

    if mode== 'Analytics':
            st.markdown('<h1 style="text-align: center;">Analytics Mode</h1>', unsafe_allow_html=True)
            st.markdown("---")

            uploaded_file = st.file_uploader("Upload a CSV file containing marketing content", type=["csv"])

            if st.button("Upload Analytics"):
                st.warning("Upload Analytics is not implemented yet.")

           

            pdf_buffer = None  
            if st.button("Extract Analytics"):
                if uploaded_file:
                    pdf_buffer = handle_analytics(uploaded_file)
                else:
                    st.error("Please upload a CSV file before extracting analytics.")

            if pdf_buffer:
                st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_buffer,
                    file_name="extracted_data.pdf",
                    mime="application/pdf"
        )

    if mode == "Trends":
        st.markdown('<h1 style="text-align: center;">Trends Mode</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        analytics_model = st.selectbox("Select Analytics Type", ["Google Trends", "Google Search"])
        
        query = st.chat_input("Enter your analytics query")
        
        if query:
            if analytics_model == "Google Search":
                with st.spinner('Fetching Google Search results...'):
                    results = handle_google_search(query)
                st.markdown("### Google Search Results")
                for result in results:
                    st.write(f"- {result}")
            
            elif analytics_model == "Google Trends":
                with st.spinner('Fetching Google Trends...'):
                    plot_file_path = handle_google_trends(query)
                
                if plot_file_path:
                    with open(plot_file_path, "rb") as file:
                        btn = st.download_button(
                            label="📥 Download Trends Plot",
                            data=file,
                            file_name=f"{os.path.basename(plot_file_path)}",
                            mime="image/png"
                        )
    if mode == "Editor":
        st.markdown('<h1 style="text-align: center;">Editor Mode</h1>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Cropping Tool")

        img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
        realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
        box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
        aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
        aspect_dict = {
            "1:1": (1, 1),
            "16:9": (16, 9),
            "4:3": (4, 3),
            "2:3": (2, 3),
            "Free": None
        }
        aspect_ratio = aspect_dict[aspect_choice]

        cropped_img = handle_cropper(img_file, realtime_update, box_color, aspect_ratio)

        if cropped_img:
            st.write("Preview")
            _ = cropped_img.thumbnail((150, 150))
            st.image(cropped_img)

            if st.button("💾 Save Cropped Image"):
                if "saved_images" not in st.session_state:
                    st.session_state.saved_images = []

                image_path = f"./saved_cropped_{len(st.session_state.saved_images) + 1}.png"
                cropped_img.save(image_path)

                st.session_state.saved_images.append(image_path)
                st.success("Cropped image saved successfully!")
                st.rerun()
        st.sidebar.markdown("---")

    if mode == "Canvas":
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
        )

        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
        stroke_color = st.sidebar.color_picker("Stroke color hex: ")
        bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
        bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
        realtime_update = st.sidebar.checkbox("Update in realtime", True)

        point_display_radius = None
        if drawing_mode == 'point':
            point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)

        st.markdown('<h1 style="text-align: center;">Canvas Mode</h1>', unsafe_allow_html=True)
        st.markdown("---")

        canvas_image, canvas_objects = handle_canvas(drawing_mode, stroke_width, stroke_color, bg_color, bg_image, realtime_update, point_display_radius)

        if canvas_image is not None:
            st.image(canvas_image)
            if st.button("💾 Save Canvas"):
                image_path = f"./saved_canvas_{len(st.session_state.get('saved_images', [])) + 1}.png"
                cv2.imwrite(image_path, canvas_image)
                
                if "saved_images" not in st.session_state:
                    st.session_state.saved_images = []
                st.session_state.saved_images.append(image_path)
                st.success("Canvas saved successfully!")
                st.rerun()

        if canvas_objects is not None:
            st.dataframe(canvas_objects)

        st.sidebar.markdown("---")

    if mode == "Calendar":
        st.markdown('<h1 style="text-align: center;">Calendar Mode</h1>', unsafe_allow_html=True)
        st.markdown("---")
        handle_calendar()

    st.sidebar.markdown('<div class="logout-button-container">', unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()  
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    logging.info("Streamlit page configured and title set.")

if __name__ == "__main__":
    setup_interface()



