from app.model.canvas_model import draw_canvas, process_canvas_result
import numpy as np
import cv2

def handle_canvas(drawing_mode, stroke_width, stroke_color, bg_color, bg_image, realtime_update, point_display_radius=None):
    canvas_result = draw_canvas(drawing_mode, stroke_width, stroke_color, bg_color, bg_image, realtime_update, point_display_radius)
    
    image_data, objects_data = process_canvas_result(canvas_result)
    
    image_to_save = None 
    
    if image_data is not None:
        image_to_save = cv2.cvtColor(np.array(image_data), cv2.COLOR_RGBA2RGB)
    
    return image_to_save, objects_data

