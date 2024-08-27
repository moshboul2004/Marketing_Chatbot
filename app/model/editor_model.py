
from PIL import Image
from streamlit_cropper import st_cropper

def crop_image(img, realtime_update, box_color, aspect_ratio):
    cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color, aspect_ratio=aspect_ratio)
    return cropped_img
