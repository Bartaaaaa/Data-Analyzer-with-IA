from django.urls import path
from src.views.SpotifyView import spotify_login, spotify_callback, check_spotify_token

urlpatterns = [
    path("api/spotify/auth/login", spotify_login, name="spotify-login"),
    path("api/spotify/auth/callback", spotify_callback, name="spotify-callback"),
    path("api/spotify/checkToken", check_spotify_token, name="spotify-checkToken"),
]