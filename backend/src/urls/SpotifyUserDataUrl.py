from django.urls import path
from src.views.SpotifyUserDataView import (
    SpotifyTopArtists
)

urlpatterns = [
    path("topArtists", SpotifyTopArtists.as_view(), name="spotify-topArtists"),
]
