import requests
from datetime import timedelta
from django.utils import timezone
from src.models.SpotifyTokenModel import SpotifyToken
import os
import base64

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded",
}

def refresh_spotify_token(user):
    try:
        token = SpotifyToken.objects.get(user=user)
    except SpotifyToken.DoesNotExist:
        return None
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token.refresh_token,
    }

    token_url = "https://accounts.spotify.com/api/token"
    refreshRequest = requests.post(token_url, headers=headers, data=data, verify=False)
    if refreshRequest.status_code != 200:
        return None

    new_token = refreshRequest.json()
    token.access_token = new_token['access_token']
    token.expires_at = timezone.now() + timedelta(seconds=new_token['expires_in'])
    token.save()
    return token.access_token


class SpotifyTokenMixin:
    def getValidSpotifyToken(self, user):
        try :
            token = SpotifyToken.objects.get(user=user)
        except SpotifyToken.DoesNotExist :
            return None
        if token.expires_at <= timezone.now() :
            new_access_token = refresh_spotify_token(user)
            if new_access_token:
                token.refresh_from_db()
            else :
                return None
        return token.access_token
