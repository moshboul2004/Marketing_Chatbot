from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import utils



def generate_pdf(chat_history):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y_position = height - 40
    for line in chat_history.split('\n'):
        p.drawString(40, y_position, line)
        y_position -= 15
        if y_position < 40:
            p.showPage()
            y_position = height - 40

    p.save()
    buffer.seek(0)
    return buffer



def draw_wrapped_text(p, text, x, y, max_width):
    """
    Draws text on the canvas, wrapping it to fit within the specified width.
    """
    text_object = p.beginText(x, y)
    text_object.setFont("Helvetica", 12)
    text_object.setTextOrigin(x, y)
    text_object.textLines(utils.simpleSplit(text, p._fontname, p._fontsize, max_width))
    p.drawText(text_object)

def generate_pdf_with_caption(posts):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    for post in posts:
        img = Image.open(post['image_path'])
        img_width, img_height = img.size

        ratio = min((width - 80) / img_width, (height - 200) / img_height)
        img_width = int(img_width * ratio)
        img_height = int(img_height * ratio)

        x_position = (width - img_width) // 2
        y_position = height - img_height - 100

        p.drawImage(post['image_path'], x_position, y_position, img_width, img_height)

        caption_position = y_position - 30
        draw_wrapped_text(p, post['caption'], 40, caption_position, width - 80)
        p.showPage()

    p.save()
    buffer.seek(0)
    return buffer

def create_pdf_from_text(insights):
    """
    Generates a PDF containing only the insights.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y_position = height - 40

    p.drawString(40, y_position, "Insights:")
    y_position -= 20
    for line in insights.split('\n'):
        p.drawString(40, y_position, line)
        y_position -= 15
        if y_position < 40:
            p.showPage()
            y_position = height - 40

    p.save()
    buffer.seek(0)
    return buffer