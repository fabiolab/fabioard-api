import datetime
import os

import pendulum
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from fabioard.domain.business.event import Event
from fabioard.domain.protocol.calendar_provider_protocol import CalendarProviderProtocol

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalendarProvider(CalendarProviderProtocol):
    def __init__(self):
        self.calendar_service = build('calendar', 'v3', credentials=self._get_credentials())

    def get_events(self, calendar_id: str) -> list[Event]:
        now = datetime.datetime.now().isoformat() + 'Z'  # 'Z' for UTC time
        events_result = self.calendar_service.events().list(
            calendarId=calendar_id, timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()

        return [Event(summary=event['summary'],
                      start=pendulum.parse(event['start'].get('date')),
                      end=pendulum.parse(event['end'].get('date')))
                for event in events_result.get('items', [])]

    def get_calendar_list(self) -> list[str]:
        return [cal['id'] for cal in self.calendar_service.calendarList().list().execute().get('items', [])]

    @staticmethod
    def _get_credentials() -> dict:
        creds = None
        # credentials.json stores user access and refresh tokens
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # if no valid credentials are available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save credentials for next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return creds
