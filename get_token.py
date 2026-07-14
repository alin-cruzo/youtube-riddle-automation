"""Get YouTube Refresh Token"""

import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    
    # Save refresh token
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)
    
    print("=" * 50)
    print("SAVE THESE VALUES TO GITHUB SECRETS:")
    print("=" * 50)
    print("YOUTUBE_CLIENT_ID: " + credentials.client_id)
    print("YOUTUBE_CLIENT_SECRET: " + credentials.client_secret)
    print("YOUTUBE_REFRESH_TOKEN: " + str(credentials.refresh_token))
    print("=" * 50)
    print("Also saved to token.pickle for local use")
    return credentials

if __name__ == "__main__":
    get_credentials()
