from googleapiclient.discovery import build
from google.oauth2 import service_account
from backend.config import setting
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import dateparser


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    cred = service_account.Credentials.from_service_account_file(
        setting.GOOGLE_CREDENTIAL_PATH, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=cred)

def book_slots(summary, start_time, end_time):
    if not all([summary, start_time, end_time]):
        return " Missing required details for booking."
    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }

    try:
        created_event = service.events().insert(
            calendarId=setting.GOOGLE_CALENDAR_ID,
            body=event
        ).execute()

        event_link = created_event.get('htmlLink')
        event_start = created_event["start"].get("dateTime", created_event["start"].get("date"))
        event_end = created_event["end"].get("dateTime", created_event["end"].get("date"))

        return f"""
        📅 **Event Booked!**  
        ✅ *"{summary}"* has been scheduled.  
        🕒 **Time:** {event_start} – {event_end}  
        🔗 [**View it on Google Calendar**]({event_link})
        """

    except Exception as e:
        return f" Failed to book event: {str(e)}"

def get_booked_slots(days_till):
    service = get_calendar_service()

    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    time_min = now.isoformat() 
    time_max = (now + timedelta(days=days_till)).isoformat()

    event_result = service.events().list(
        calendarId=setting.GOOGLE_CALENDAR_ID,
        timeMin = time_min,
        timeMax = time_max,
        singleEvents = True,
        orderBy = "startTime"
    ).execute()


    events = event_result.get('items', [])


    if not events:
        return "No events found"
    
    
    result = "Booked slots"
    for e in events:
        start = e["start"].get("dateTime", e['start'].get("date"))
        end = e["end"].get("dateTime", e["end"].get("date"))
        title = e.get('summary', 'untitled')
        link = e.get('htmlLink')
        result += f" --> {title} from {start} to {end} and view details {link}"

    return result



def suggest_available_slots(duration):

    service = get_calendar_service()

    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    start_time = now.replace(hour=9, minute=0, second=0)
    end_time = now.replace(hour=21, minute=0, second=0)

    min_time = start_time.isoformat()
    max_time = end_time.isoformat()

    events_list = service.events().list(
        calendarId=setting.GOOGLE_CALENDAR_ID,
        timeMin = min_time,
        timeMax = max_time,
        singleEvents = True,
        orderBy = "startTime"
    ).execute().get("items", [])

    busy = [(start_time, start_time)]

    for e in events_list:

        start = datetime.fromisoformat(e["start"]["dateTime"])
        end = datetime.fromisoformat(e['end']["dateTime"])
        busy.append((start, end))

    busy.append((end_time, end_time))
    busy.sort()


    for i in range(len(busy)-1):
        gap_st= busy[i][1]
        gap_end = busy[i+1][0]
        free_time = (gap_end - gap_st).total_seconds()/60
        if free_time >= duration:
            return f"suggestion {gap_st.strftime("%Y-%m-%d %H:%M")} to {gap_end.strftime("%Y-%m-%d %H:%M")}" 
        
        else:
            return "no available slots "

    


        


