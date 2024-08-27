from datetime import datetime

def get_current_date_and_time():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_time = now.strftime("%H:%M:%S")

    return formatted_date, formatted_time