from django.urls import path
from src.views.SpotifyUserDataView import (
    SpotifyTopArtists,
    SpotifyTopTracks,
    SpotifyCurrentTrack,
    SpotifySkipToNext,
    SpotifySkipToPrevious,
    SpotifyPauseTrack,
    SpotifyResumeTrack
)

urlpatterns = [
    path("topArtists", SpotifyTopArtists.as_view(), name="spotify-topArtists"),
    path("topTracks", SpotifyTopTracks.as_view(), name="spotify-topTracks"),
    path("currentTrack", SpotifyCurrentTrack.as_view(), name="spotify-currentlyPlayingTrack"),
    path("skipNextTrack", SpotifySkipToNext.as_view(), name="spotify-skipToNext"),
    path("skipPreviousTrack", SpotifySkipToPrevious.as_view(), name="spotify-skipToPrevious"),
    path("SpotifyPauseTrack", SpotifyPauseTrack.as_view(), name="spotify-pauseTrack"),
    path("SpotifyResumeTrack", SpotifyResumeTrack.as_view(), name="spotify-resumeTrack"),

]
