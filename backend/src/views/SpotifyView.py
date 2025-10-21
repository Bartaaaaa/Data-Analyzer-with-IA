# myapp/views.py
import os
import base64
import requests
from urllib.parse import urlencode
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import timedelta
from django.utils import timezone
from src.models.SpotifyTokenModel import SpotifyToken
from rest_framework_simplejwt.authentication import JWTAuthentication

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded",
}


def spotify_login(request):
    jwt_token = request.GET.get("jwt")
    if not jwt_token:
        return JsonResponse({"error": "JWT not provided"}, status=401)

    scopes = "user-top-read user-read-recently-played"
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": scopes,
        "redirect_uri": REDIRECT_URI,
        "state": jwt_token,
    }
    url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return HttpResponseRedirect(url)


def spotify_callback(request):
    code = request.GET.get("code")
    jwt_token = request.GET.get("state")
    jwt_auth = JWTAuthentication()

    try:
        validated_token = jwt_auth.get_validated_token(jwt_token)
        user = jwt_auth.get_user(validated_token)
    except Exception:
        return JsonResponse({"error": "Invalid JWT"}, status=401)

    # --- Échange du code Spotify contre les tokens
    token_url = "https://accounts.spotify.com/api/token"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    spotifyTokenRequest = requests.post(token_url, headers=headers, data=data, verify=False)
    if spotifyTokenRequest.status_code != 200:
        return JsonResponse({"error": "token request failed", "details": spotifyTokenRequest.text}, status=400)

    tokens = spotifyTokenRequest.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in")
    expires_at = timezone.now() + timedelta(seconds=expires_in)

    SpotifyToken.objects.update_or_create(
        user=user,
        defaults={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
        },
    )

    frontend = "http://localhost:4200/connections"
    return HttpResponseRedirect(f"{frontend}?spotify_connected=1")

def refresh_spotify_token(user):
    try :
        token = SpotifyToken.objects.get(user=user)
    except SpotifyToken.DoesNotExist:
        return None
    refresh_token = token.refresh_token
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    spotifyTokenRequest = requests.post(token_url, headers=headers, data=data, verify=False)
    if spotifyTokenRequest.status_code != 200:
        print("refresh token request failed", spotifyTokenRequest.text)
        return None
    newToken = spotifyTokenRequest.json()
    access_token = newToken.get("access_token")
    expires_in = newToken.get("expires_in")
    token.access_token = access_token
    token.expires_at = timezone.now() + timedelta(seconds=expires_in)
    token.save()
    return access_token

def check_spotify_token(user):
    try :
        token = SpotifyToken.objects.get(user=user)
    except SpotifyToken.DoesNotExist:
        return None # Utilisateur s'est jamais connecté
    if token.expires_at < timezone.now():
        refresh_spotify_token(user)
    return True