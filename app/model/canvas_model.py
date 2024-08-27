import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas

def draw_canvas(drawing_mode, stroke_width, stroke_color, bg_color, bg_image, realtime_update, point_display_radius=None):
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        width=800,
        height=300,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="canvas",
    )
    
    return canvas_result

def process_canvas_result(canvas_result):
    image_data = None
    objects_data = None

    if canvas_result.image_data is not None:
        image_data = canvas_result.image_data

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.select_dtypes(include=['object']).columns:
            objects[col] = objects[col].astype("str")
        objects_data = objects

    return image_data, objects_data
