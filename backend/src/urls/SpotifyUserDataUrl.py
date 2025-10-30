from django.urls import path
from src.views.SpotifyUserDataView import (
    SpotifyTopArtists,
    SpotifyTopTracks
)

urlpatterns = [
    path("topArtists", SpotifyTopArtists.as_view(), name="spotify-topArtists"),
    path("topTracks", SpotifyTopTracks.as_view(), name="spotify-topTracks"),
]
