
#code for using calendar data to generate user profile
# import os
# import pickle
# import datetime
# import re
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build

# # If modifying these SCOPES, delete the token.pickle file.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# def authenticate_google_calendar():
    
#     creds = None
#     # The token.pickle stores the user's access and refresh tokens and is created automatically when the authorization flow completes..
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
    
#     # If there are no valid credentials, allow the user to log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'client_secret_381614316257-l3rpl2im6h094a2rorr89j68ucfegoif.apps.googleusercontent.com.json', SCOPES)
#             creds = flow.run_local_server(port=0)
        
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
    
#     return creds

# def get_calendar_events():
#     # Authenticate and build the service
#     creds = authenticate_google_calendar()
#     service = build('calendar', 'v3', credentials=creds)

#     # Call the Calendar API to get events from the primary calendar
#     now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                           maxResults=10, singleEvents=True,
#                                           orderBy='startTime').execute()
#     events = events_result.get('items', [])
    
#     return events

# def clean_description(description):
#     # Remove any HTML tags or links (anything starting with 'http' or '<a>')
#     description = re.sub(r'<a.*?>.*?</a>', '', description)  # Remove HTML links
#     description = re.sub(r'http\S+', '', description)  # Remove URLs
#     description = re.sub(r'\s+', ' ', description).strip()  # Remove extra spaces/newlines
#     return description

# def save_events_to_txt(events, filename='calendar_events.txt'):
#     with open(filename, 'w') as file:
#         if not events:
#             file.write("No upcoming events found.\n")
#         else:
#             for event in events:
#                 event_details = f"Event: {event['summary']}\n"
                
#                 # Only include description if it exists and is not empty after cleaning
#                 if 'description' in event:
#                     clean_desc = clean_description(event['description'])
#                     if clean_desc:  # Only print description if it's not empty
#                         event_details += f"Description: {clean_desc}\n"
                
#                 event_details += "\n"  # Add a blank line between events
#                 file.write(event_details)
                
#     print(f"Events saved to {filename}")

# if __name__ == '__main__':
#     # Get the events and save them to a file
#     events = get_calendar_events()
#     save_events_to_txt(events)


#code for check avalability based on user query
import spacy
import datetime
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import pytz
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import dateparser

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# Google Calendar API SCOPES
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def parse_query_with_nlp(query):
    """
    Use NLP to interpret user queries and extract start/end dates or durations.
    """
    doc = nlp(query.lower())
    today = datetime.datetime.now()
    start_date, end_date = today, today
    duration = 0

    # Recognize intent and extract key details
    for ent in doc.ents:
        if ent.label_ == "DATE":
            parsed_date = parse_date(ent.text, today)
            if parsed_date:
                start_date = parsed_date
                end_date = start_date

        elif ent.label_ == "CARDINAL":
            # Handle durations like "3 days", "4 weeks", etc.
            match = re.search(r"(\d+)\s*(day|days|week|weeks)", query)
            if match:
                number = int(match.group(1))
                unit = match.group(2)
                duration = number * (7 if "week" in unit else 1) - 1
                end_date = start_date + datetime.timedelta(days=duration)

        

        # Handle complex patterns (e.g., "weekend trip")
        elif "weekend" in query:
            start_date = calculate_next_weekday(today, "friday")
            end_date = start_date + datetime.timedelta(days=2)

        elif "summer" in query:
            start_date, end_date = handle_season("summer", today)
        elif "winter" in query:
            start_date, end_date = handle_season("winter", today)

    # Default to 1-day trip if duration is unclear
    # if start_date == end_date:
    #     end_date = start_date + datetime.timedelta(days=1)

    if duration > 0 and start_date == end_date:
        end_date = start_date + datetime.timedelta(days=duration)

    return start_date, end_date

# def parse_date(text, today):
#     """
#     Attempt to parse natural language dates into datetime objects.
#     """
#     try:
#         # First try direct parsing (e.g., "January 17")
#         return datetime.datetime.strptime(text, "%d %B %Y")
#     except ValueError:
#         pass

#     # Handle relative dates like "next Monday"
#     if "next" in text or "on" in text:
#         day_name = re.search(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", text)
#         if day_name:
#             return calculate_next_weekday(today, day_name.group())

#     # Add other parsing logic as needed
#     return None

def parse_date(text, today):
    parsed_date = dateparser.parse(text, settings={'RELATIVE_BASE': today})
    return parsed_date if parsed_date else None

def calculate_next_weekday(start_date, weekday_name):
    """
    Calculate the next occurrence of a given weekday.
    """
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    target_weekday = weekdays.index(weekday_name.lower())
    current_weekday = start_date.weekday()
    days_ahead = (target_weekday - current_weekday + 7) % 7 or 7
    return start_date + datetime.timedelta(days=days_ahead)

def handle_season(season, today):
    """
    Define date ranges for seasonal references.
    """
    if season == "summer":
        return today.replace(month=6, day=1), today.replace(month=8, day=31)
    elif season == "winter":
        if today.month in [12, 1, 2]:
            return today.replace(month=12 if today.month == 12 else 1, day=1), today.replace(month=2, day=28)
    return today, today

# def authenticate_google_calendar():
#     """
#     Authenticate and build the Google Calendar API client.
#     """
#     creds = None
#     if 'token.json' in os.listdir():
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'cse.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     return creds


def authenticate_google_calendar():
    creds = None
    token_path = 'token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Build the service object
    service = build('calendar', 'v3', credentials=creds)
    return service

# def get_events_for_date_range(start_date, end_date):
#     """
#     Fetch events from Google Calendar for a specified date range.
#     """
#     creds = authenticate_google_calendar()
#     service = build('calendar', 'v3', credentials=creds)
#     events_result = service.events().list(calendarId='primary', timeMin=start_date.isoformat(), timeMax=end_date.isoformat(), singleEvents=True, orderBy='startTime').execute()
#     return events_result.get('items', [])


# def get_events_for_date_range(start_date, end_date):
#     # Assuming 'start_date' and 'end_date' are naive datetimes
#     tz = pytz.timezone('UTC')  # Replace with your desired timezone
#     start_date = tz.localize(start_date)
#     end_date = tz.localize(end_date)
    
#     service = authenticate_google_calendar()
    
#     events_result = service.events().list(
#         calendarId='primary',
#         timeMin=start_date.isoformat(),
#         timeMax=end_date.isoformat(),
#         singleEvents=True,
#         orderBy='startTime'
#     ).execute()
    
#     events = events_result.get('items', [])
#     return events

# def get_events_for_date_range(start_date, end_date):
#     service = authenticate_google_calendar()  # Make sure to call this properly
#     events_result = service.events().list(
#         calendarId='primary',
#         timeMin=start_date.isoformat() + 'Z',  # Add 'Z' for UTC timezone
#         timeMax=end_date.isoformat() + 'Z',
#         singleEvents=True,
#         orderBy='startTime'
#     ).execute()
#     events = events_result.get('items', [])
#     return events

def get_events_for_date_range(start_date, end_date):
    tz = pytz.UTC  # Adjust as per your local timezone
    start_date = tz.localize(start_date)
    end_date = tz.localize(end_date)

    service = authenticate_google_calendar()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_date.isoformat(),
        timeMax=end_date.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])

# def find_availability(events, start_date, end_date):
#     """
#     Find available slots for travel by checking Google Calendar events.
#     """
#     availability = []
#     current_time = start_date
#     for event in events:
#         event_start = datetime.datetime.fromisoformat(event['start']['dateTime'])
#         event_end = datetime.datetime.fromisoformat(event['end']['dateTime'])

#         if current_time < event_start:
#             availability.append((current_time, event_start))
#         current_time = max(current_time, event_end)

#     if current_time < end_date:
#         availability.append((current_time, end_date))

#     return availability

def find_availability(events, start_date, end_date):
    availability = []
    current_time = start_date

    for event in events:
        event_start = datetime.datetime.fromisoformat(event['start'].get('dateTime', event['start']['date']))
        event_end = datetime.datetime.fromisoformat(event['end'].get('dateTime', event['end']['date']))

        if current_time < event_start:
            availability.append((current_time, event_start))
        current_time = max(current_time, event_end)

    if current_time < end_date:
        availability.append((current_time, end_date))

    return availability


def main():
    query = input("Enter your query: ").strip()
    start_date, end_date = parse_query_with_nlp(query)

    # Fetch events from Google Calendar
    events = get_events_for_date_range(start_date, end_date)

    # Find availability
    availability = find_availability(events, start_date, end_date)

    # Display results
    print(f"Available slots from {start_date.date()} to {end_date.date()}:")
    if not availability:
        print("No available slots.")
    else:
        for slot in availability:
            print(f"From {slot[0]} to {slot[1]}")

if __name__ == "__main__":
    main()

