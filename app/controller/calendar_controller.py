
from app.model.calendar_model import create_calendar

def handle_calendar():
    calendar_options = {
        "editable": "true",
        "selectable": "true",
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialView": "dayGridMonth",  
        "slotMinTime": "06:00:00",
        "slotMaxTime": "18:00:00",
        "height": "auto",  
        "contentHeight": "parent",  
        "expandRows": True,  
    }

    calendar_events = [
        {
            "title": "Event 1",
            "start": "2023-07-31T08:30:00",
            "end": "2023-07-31T10:30:00",
        },
        {
            "title": "Event 2",
            "start": "2023-07-31T07:30:00",
            "end": "2023-07-31T10:30:00",
        },
        {
            "title": "Event 3",
            "start": "2023-07-31T10:40:00",
            "end": "2023-07-31T12:30:00",
        }
    ]

    custom_css = """
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
        .fc-daygrid-body tr:last-child {
            border-bottom: 1px solid #ddd;
        }
    """

    calendar_component = create_calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
    return calendar_component
