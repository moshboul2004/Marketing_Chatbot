
from app.model.editor_model import crop_image
from PIL import Image

def handle_cropper(img_file, realtime_update, box_color, aspect_ratio):
    if img_file:
        img = Image.open(img_file)
        cropped_img = crop_image(img, realtime_update, box_color, aspect_ratio)
        return cropped_img
    return None
