from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'ansh.verma.av0608@gmail.com'  # or your actual calendar 

def get_calendar_service():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    return service

def check_availability(date: str):
    """
    Checks free time slots on a given date (YYYY-MM-DD).
    """
    service = get_calendar_service()

    start_datetime = datetime.fromisoformat(date)
    end_datetime = start_datetime + timedelta(days=1)

    body = {
        "timeMin": start_datetime.isoformat() + 'Z',
        "timeMax": end_datetime.isoformat() + 'Z',
        "items": [{"id": CALENDAR_ID}]
    }

    events_result = service.freebusy().query(body=body).execute()
    busy_slots = events_result['calendars'][CALENDAR_ID]['busy']

    return busy_slots if busy_slots else "You’re free all day!"

def book_event(summary: str, date: str, time: str, duration_minutes=30):
    """
    Books a meeting on the calendar with given summary, date (YYYY-MM-DD), and time (HH:MM).
    """
    service = get_calendar_service()

    start_datetime = datetime.fromisoformat(f"{date}T{time}")
    end_datetime = start_datetime + timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"Meeting booked: {created_event.get('htmlLink')}"
