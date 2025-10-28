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
        params = {"limit" : 10, "time_range": "medium_term"}
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

