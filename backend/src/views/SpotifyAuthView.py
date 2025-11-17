# src/views/SpotifyView.py
import requests
from urllib.parse import urlencode
from django.http import HttpResponseRedirect, JsonResponse
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from src.models.SpotifyTokenModel import SpotifyToken
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from src.utils.Spotify.SpotifyTokenHelper import SpotifyTokenMixin
from src.utils.Spotify.SpotifySettings import HEADERS, AUTH_HEADER, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

@extend_schema(tags=['SpotifyAuth'])
class SpotifyLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        jwt_token = request.GET.get("jwt")
        if not jwt_token:
            return JsonResponse({"error": "JWT required"}, status=401)
        #Routes that i can call from spotify
        scopes = "user-top-read user-read-recently-played user-read-currently-playing user-modify-playback-state"
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "scope": scopes,
            "redirect_uri": REDIRECT_URI,
            "state": jwt_token,
        }
        url = "https://accounts.spotify.com/authorize?" + urlencode(params)
        return HttpResponseRedirect(url)

@extend_schema(tags=['SpotifyAuth'])
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
        r = requests.post(token_url, headers=HEADERS, data=data, verify=False)

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

@extend_schema(tags=['SpotifyAuth'])
class SpotifyCheckTokenView(APIView):
    def get(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)

        if access_token:
            return JsonResponse({"isConnected": True})
        return JsonResponse({"isConnected": False})

