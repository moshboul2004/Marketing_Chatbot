
from streamlit_calendar import calendar

def create_calendar(events, options, custom_css=None):
    calendar_component = calendar(events=events, options=options, custom_css=custom_css)
    return calendar_component
