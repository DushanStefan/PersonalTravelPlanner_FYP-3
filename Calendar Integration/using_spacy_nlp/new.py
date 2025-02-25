

# import spacy
# import pytz
# import datetime
# import re
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# import os
# import dateparser
# from dateutil.parser import parse  # Import parse from dateutil.parser

# # Load spaCy language model
# nlp = spacy.load("en_core_web_sm")

# # Google Calendar API SCOPES
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# def parse_query_with_nlp(query):
#     """
#     Use NLP to interpret user queries and extract start/end dates or durations.
#     """
#     doc = nlp(query.lower())
#     today = datetime.datetime.now()
#     start_date, end_date = today, today
#     duration = 0

#     # Extract dates using NLP
#     for ent in doc.ents:
#         if ent.label_ == "DATE":
#             parsed_date = parse_date(ent.text, today)
#             if parsed_date:
#                 start_date = parsed_date
#                 end_date = start_date

#     # Extract duration using a regex (e.g., "3 days", "3-day", "2 weeks")
#     match = re.search(r"(\d+)[\s-]*(day|days|week|weeks)", query)
#     if match:
#         number = int(match.group(1))
#         unit = match.group(2)
#         duration = number * (7 if "week" in unit else 1)
#         end_date = start_date + datetime.timedelta(days=duration - 1)

#     # Default to a 1-day trip if duration is not provided
#     if duration == 0:
#         end_date = start_date + datetime.timedelta(days=1)

#     # Debugging output
#     print(f"Query: {query}")
#     print(f"Detected start_date: {start_date}")
#     print(f"Detected end_date: {end_date}")
#     print(f"Detected duration: {duration}")

#     return start_date, end_date




# def parse_date(text, today):
#     """
#     Parse date from text using dateparser with enhanced settings and fallback for specific patterns.
#     """
#     # Force handling of specific formats if dateparser fails
#     try:
#         if "15th of march" in text.lower():
#             return datetime.datetime(today.year, 3, 15)
#     except Exception as e:
#         print(f"Error in custom handling: {e}")

#     # Use dateparser with specific settings
#     parsed_date = dateparser.parse(
#         text,
#         settings={'RELATIVE_BASE': today, 'PREFER_DATES_FROM': 'future'}
#     )

#     if not parsed_date:
#         try:
#             # Fallback: Use dateutil.parser as a backup
#             parsed_date = parse(text, fuzzy=True)
#         except (ValueError, TypeError):
#             return None

#     return parsed_date




# def authenticate_google_calendar():
#     creds = None
#     token_path = 'token.json'
#     if os.path.exists(token_path):
#         creds = Credentials.from_authorized_user_file(token_path, SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('cse.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open(token_path, 'w') as token:
#             token.write(creds.to_json())

#     # Build the service object
#     service = build('calendar', 'v3', credentials=creds)
#     return service

# def get_events_for_date_range(start_date, end_date):
#     tz = pytz.UTC  # Adjust as per your local timezone
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

#     return events_result.get('items', [])

# def find_availability(events, start_date, end_date):
#     availability = []
#     current_time = start_date

#     # Local timezone (system's local timezone)
#     local_tz = pytz.timezone("Asia/Colombo") # You can change this to your preferred timezone

#     for event in events:
#         # Convert event times to UTC first, then to local timezone (naive datetime)
#         event_start = datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(local_tz).replace(tzinfo=None)
#         event_end = datetime.datetime.fromisoformat(event['end']['dateTime']).astimezone(local_tz).replace(tzinfo=None)

#         # Compare and find availability
#         if current_time < event_start:
#             availability.append((current_time, event_start))
#         current_time = max(current_time, event_end)

#     if current_time < end_date:
#         availability.append((current_time, end_date))

#     return availability

# def main():
#     query = input("Enter your query: ").strip()
#     start_date, end_date = parse_query_with_nlp(query)

#     # Fetch events from Google Calendar
#     events = get_events_for_date_range(start_date, end_date)

#     # Find availability
#     availability = find_availability(events, start_date, end_date)

#     # Display results
#     print(f"Available slots from {start_date.date()} to {end_date.date()}:")
#     if not availability:
#         print("No available slots.")
#     else:
#         for slot in availability:
#             # Ensure the datetime is naive and local
#             start_time_naive = slot[0].replace(tzinfo=None)
#             end_time_naive = slot[1].replace(tzinfo=None)

#             # Print the slots as naive local times
#             print(f"From {start_time_naive} to {end_time_naive}")

# if __name__ == "__main__":
#     main()



import spacy
import pytz
import datetime
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import dateparser
from dateutil.parser import parse  # Import parse from dateutil.parser

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
    start_date, end_date = None, None
    duration = 0

    # Extract dates using NLP (this will get actual date phrases)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            parsed_date = parse_date(ent.text, today)
            if parsed_date:
                start_date = parsed_date
                print(f"Found date in query: {start_date}")

    # Now extract duration from the query if present
    duration_match = re.search(r"(\d+)[\s-]*(day|days|week|weeks)", query)
    if duration_match:
        number = int(duration_match.group(1))
        unit = duration_match.group(2)
        duration = number * (7 if "week" in unit else 1)
        print(f"Found duration in query: {duration} days")

    # If no start_date was found, default to today
    if not start_date:
        start_date = today
        print(f"No date found in query. Using today as start date: {start_date}")

    # Calculate end_date based on the duration
    if duration > 0:
        end_date = start_date + datetime.timedelta(days=duration - 1)
    else:
        end_date = start_date + datetime.timedelta(days=1)  # Default to 1 day

    # Debugging output
    print(f"Query: {query}")
    print(f"Detected start_date: {start_date}")
    print(f"Detected end_date: {end_date}")
    print(f"Detected duration: {duration}")

    return start_date, end_date

def parse_date(text, today):
    """
    Parse date from text using dateparser with enhanced settings and fallback for specific patterns.
    """
    try:
        # Specific phrases handling
        text = text.lower()
        if "2nd of february" in text:
            return datetime.datetime(today.year, 2, 2)
        if "15th of february" in text:
            return datetime.datetime(today.year, 2, 15)

        # General parsing using dateparser
        parsed_date = dateparser.parse(
            text,
            settings={'RELATIVE_BASE': today, 'PREFER_DATES_FROM': 'future'}
        )

        # Fallback: Use dateutil.parser if dateparser fails
        if not parsed_date:
            parsed_date = parse(text, fuzzy=True)

        return parsed_date

    except (ValueError, TypeError, Exception) as e:
        print(f"Error parsing date '{text}': {e}")
        return None

def authenticate_google_calendar():
    creds = None
    token_path = 'token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('cse.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Build the service object
    service = build('calendar', 'v3', credentials=creds)
    return service

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

def find_availability(events, start_date, end_date):
    availability = []
    current_time = start_date

    # Local timezone (system's local timezone)
    local_tz = pytz.timezone("Asia/Colombo")  # You can change this to your preferred timezone

    for event in events:
        # Convert event times to UTC first, then to local timezone (naive datetime)
        event_start = datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(local_tz).replace(tzinfo=None)
        event_end = datetime.datetime.fromisoformat(event['end']['dateTime']).astimezone(local_tz).replace(tzinfo=None)

        # Compare and find availability
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
            # Ensure the datetime is naive and local
            start_time_naive = slot[0].replace(tzinfo=None)
            end_time_naive = slot[1].replace(tzinfo=None)

            # Print the slots as naive local times
            print(f"From {start_time_naive} to {end_time_naive}")

if __name__ == "__main__":
    main()
