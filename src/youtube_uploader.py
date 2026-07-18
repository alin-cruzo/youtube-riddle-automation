"""YouTube Uploader

Uses google_auth_httplib2.AuthorizedHttp to wrap an httplib2.Http instance
with an explicit timeout. The default googleapiclient setup builds an
httplib2.Http with no timeout, which can hang indefinitely on a slow/stalled
TLS handshake on some Windows networks — even when the network path itself
is fine (confirmed: Test-NetConnection succeeds, and a plain requests.get()
to the same host completes fine). Setting an explicit timeout here makes
a stalled handshake fail fast and clearly instead of hanging.
"""

import os
import httplib2
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class YouTubeUploader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    REQUEST_TIMEOUT = 120  # seconds — generous, since resumable video uploads can be slow

    def __init__(self):
        self.client_id = os.environ.get('YOUTUBE_CLIENT_ID')
        self.client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
        self.refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')

        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Missing YouTube API credentials in environment variables")

        self.service = self._get_authenticated_service()

    def _get_authenticated_service(self):
        credentials = Credentials(
            None,
            refresh_token=self.refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.SCOPES
        )
        # Refresh the access token using google-auth's own Request object
        # (this part already worked fine before; the timeout below is what
        # protects the actual API calls that come after).
        credentials.refresh(Request())

        # Build an httplib2.Http with an explicit timeout, then wrap it with
        # AuthorizedHttp so it carries our OAuth credentials on every call.
        http = httplib2.Http(timeout=self.REQUEST_TIMEOUT)
        authed_http = AuthorizedHttp(credentials, http=http)

        return build(self.API_SERVICE_NAME, self.API_VERSION, http=authed_http)

    def upload_short(self, video_path, title, description, tags, thumbnail_path=None):
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24',
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            }
        }

        media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)

        request = self.service.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print("Upload progress: " + str(int(status.progress() * 100)) + "%")

        video_id = response['id']
        print("Upload complete! Video ID: " + video_id)
        print("URL: https://youtube.com/shorts/" + video_id)

        if thumbnail_path and os.path.exists(thumbnail_path):
            self.service.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            print("Thumbnail uploaded!")

        return video_id