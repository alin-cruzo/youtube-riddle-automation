"""Get YouTube Refresh Token - Manual Flow"""

import json
import urllib.parse
from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Load client secrets
with open('client_secret.json', 'r') as f:
    client_config = json.load(f)

# Create flow
flow = Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Manual copy-paste flow
)

# Get authorization URL
auth_url, _ = flow.authorization_url(prompt='consent')

print("=" * 60)
print("OPEN THIS URL IN YOUR BROWSER:")
print("=" * 60)
print(auth_url)
print("=" * 60)
print("After signing in, Google will show you a CODE.")
print("Copy that code and paste it here.")
print("=" * 60)

# Get code from user
code = input("Enter the authorization code: ").strip()

# Exchange code for credentials
flow.fetch_token(code=code)
credentials = flow.credentials

print("\n" + "=" * 60)
print("SAVE THESE TO GITHUB SECRETS:")
print("=" * 60)
print("YOUTUBE_CLIENT_ID: " + credentials.client_id)
print("YOUTUBE_CLIENT_SECRET: " + credentials.client_secret)
print("YOUTUBE_REFRESH_TOKEN: " + str(credentials.refresh_token))
print("=" * 60)

# Save locally too
import pickle
with open('token.pickle', 'wb') as f:
    pickle.dump(credentials, f)
print("Also saved to token.pickle")
