# src/views/SpotifyView.py
import os
import base64
import requests
from urllib.parse import urlencode
from django.http import HttpResponseRedirect, JsonResponse
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from src.models.SpotifyTokenModel import SpotifyToken
from rest_framework import permissions


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
    r = requests.post(token_url, headers=headers, data=data, verify=False)

    if r.status_code != 200:
        return None

    new_token = r.json()
    token.access_token = new_token['access_token']
    token.expires_at = timezone.now() + timedelta(seconds=new_token['expires_in'])
    token.save()

    return token.access_token


class SpotifyLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        jwt_token = request.GET.get("jwt")
        if not jwt_token:
            return JsonResponse({"error": "JWT required"}, status=401)

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


class SpotifyCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        code = request.GET.get("code")
        jwt_token = request.GET.get("state")

        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(jwt_token)
            user = jwt_auth.get_user(validated_token)
        except Exception:
            return JsonResponse({"error": "Invalid JWT"}, status=401)

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }

        token_url = "https://accounts.spotify.com/api/token"
        r = requests.post(token_url, headers=headers, data=data, verify=False)

        if r.status_code != 200:
            return JsonResponse({"error": "token request failed"}, status=400)

        tokens = r.json()
        SpotifyToken.objects.update_or_create(
            user=user,
            defaults={
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token"),
                "expires_at": timezone.now() + timedelta(seconds=tokens.get("expires_in")),
            },
        )

        frontend = "http://localhost:4200/connections"
        return HttpResponseRedirect(f"{frontend}?spotify_connected=1")


class SpotifyCheckTokenView(APIView):
    def get(self, request):
        user = request.user
        try:
            token = SpotifyToken.objects.get(user=user)
        except SpotifyToken.DoesNotExist:
            return JsonResponse({"connected": False})

        if token.expires_at < timezone.now():
            refresh_spotify_token(user)

        return JsonResponse({"connected": True})
