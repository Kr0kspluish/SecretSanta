import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# 
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode

SCOPES = ['https://mail.google.com/']

def gmail_authenticate():
    """
    Authenticate to the Google API. A credentials.json file must exist.
    At first run, you will be asked to authenticate to your Google account. Then,
    the pickle module is used to save a login token. 

    Credits to https://www.thepythoncode.com/article/use-gmail-api-in-python, that
    would as well help you set up your OAuth credentials.
    """
    
    creds = None
    # First, try to re-use an existing token.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the (re-)generated token
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def build_message(sender, dest, obj, body):

    message = MIMEText(body)
    message['to'] = dest
    message['from'] = sender
    message['subject'] = obj
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_email(sender, dest, obj, body, service=None, verbose=False, dry_run=False):

    if not service:
        service = gmail_authenticate()

    if(verbose):
        print(("\
Sending the following email:\n\
{sep}\n\
    From: %s\n\
    To: %s\n\
    Object: %s\n\
    Body:\n%s\n\
{sep}\n"\
        %(sender, dest, obj, body)).format(sep='-'*40))
    
    mime_body = build_message(sender, dest, obj, body)
        
    if(not dry_run):
        return service.users().messages().send(
        userId="me",
        body=mime_body
        ).execute()