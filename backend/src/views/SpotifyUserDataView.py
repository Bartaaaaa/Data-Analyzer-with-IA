# src/views/SpotifyView.py
import os
import requests
from django.http import  JsonResponse
from rest_framework.views import APIView
from src.models.SpotifyTokenModel import SpotifyToken
from drf_spectacular.utils import extend_schema
from src.utils.Spotify.SpotifyTokenHelper import SpotifyTokenMixin

@extend_schema(tags=['SpotifyUserData'])
class SpotifyTopArtists(APIView):
    def get(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)
        headers = {"Authorization": f"Bearer {access_token}"}
        limit = int(request.GET.get("limit", 10))
        time_range = request.GET.get("time_range", "medium_term")
        params = {"limit" :limit, "time_range": time_range}
        url = "https://api.spotify.com/v1/me/top/artists"
        spotifyTopArtistRequest = requests.get(url, headers=headers, params=params, verify=False)
        data = spotifyTopArtistRequest.json()
        top_artists = [
            {
                "name": artist["name"],
                "id": artist["id"],
                "genres": artist["genres"],
                "popularity": artist["popularity"],
                "image": artist["images"][0]["url"] if artist["images"] else None,
                "spotify_url": artist["external_urls"]["spotify"],
            }
            for artist in data.get("items", [])
        ]

        return JsonResponse({"top_artists": top_artists})

@extend_schema(tags=['SpotifyUserData'])
class SpotifyTopTracks(APIView):
    def get(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)
        headers = {"Authorization": f"Bearer {access_token}"}
        limit = int(request.GET.get("limit", 10))
        time_range = request.GET.get("time_range", "medium_term")
        offset = int(request.GET.get("offset", 0))
        params = {"limit" :limit, "time_range": time_range, "offset": offset}
        url = "https://api.spotify.com/v1/me/top/tracks"
        spotifyTopTracksRequest = requests.get(url, headers=headers, params=params, verify=False)
        data = spotifyTopTracksRequest.json()
        top_tracks = [
            {
                "name": track["name"],
                "id": track["id"],
                "artists": [artist["name"] for artist in track["artists"]],
                "popularity": track["popularity"],
                "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                "album": track["album"]["name"],
                "album_type" : track["album"]["type"],
                "album_id" : track["album"]["id"],
                "album_url" : track["album"]["external_urls"]["spotify"],
                "spotify_url": track["external_urls"]["spotify"],
                "preview_url": track.get("preview_url"),
            }
            for track in data.get("items", [])
        ]

        return JsonResponse({"top_tracks": top_tracks})
