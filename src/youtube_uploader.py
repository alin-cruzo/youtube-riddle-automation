"""YouTube Uploader"""

import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class YouTubeUploader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    
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
        credentials.refresh(Request())
        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials)
    
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
