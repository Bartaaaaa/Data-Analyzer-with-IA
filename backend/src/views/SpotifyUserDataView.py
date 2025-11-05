# src/views/SpotifyView.py
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

@extend_schema(tags=['SpotifyUserData'])
@extend_schema(tags=['SpotifyUserData'])
class SpotifyCurrentTrack(APIView):
    def get(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://api.spotify.com/v1/me/player/currently-playing"

        try:
            spotifyCurrentTrackRequest = requests.get(url, headers=headers, verify=False)
        except requests.exceptions.RequestException as error:
            return JsonResponse({"error": str(error)}, status=500)

        if spotifyCurrentTrackRequest.status_code == 204:
            return JsonResponse({
                "name": "You are not playing any song at the moment",
                "artists": [],
                "image": "image_url",
                "track_url": "placeholder_url",
                "progress": 0,
                "album_name": None,
                "duration": 0,
                "timestamp": 0
            }, status=200)

        if spotifyCurrentTrackRequest.status_code != 200:
            return JsonResponse({
                "error": f"Spotify API error {spotifyCurrentTrackRequest.status_code}"
            }, status=spotifyCurrentTrackRequest.status_code)

        data = spotifyCurrentTrackRequest.json()
        item = data.get("item")
        current_track = {
            "name": item.get("name"),
            "artists": [artist.get("name") for artist in item.get("artists", [])],
            "image": item["album"]["images"][0]["url"] if item["album"].get("images") else None,
            "track_url": item["external_urls"]["spotify"],
            "progress": data.get("progress_ms", 0),
            "timestamp": data.get("timestamp", 0),
            "album_name": item["album"]["name"],
            "duration": item.get("duration_ms", 0),
        }

        return JsonResponse(current_track, status=200)


@extend_schema(tags=['SpotifyUserData'])
class SpotifySkipToNext(APIView):
    def post(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://api.spotify.com/v1/me/player/next"
        try :
            requests.post(url, headers=headers,verify=False)
        except requests.exceptions.RequestException as error :
            return JsonResponse({"error": str(error)})

        return JsonResponse({"error": "The request was successful."}, status=200)

@extend_schema(tags=['SpotifyUserData'])
class SpotifySkipToPrevious(APIView):
    def post(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://api.spotify.com/v1/me/player/previous"
        try :
            requests.post(url, headers=headers,verify=False)
        except requests.exceptions.RequestException as error :
            return JsonResponse({"error": str(error)})
        return JsonResponse({"error": "The request was successful."}, status=200)



@extend_schema(tags=['SpotifyUserData'])
class SpotifyPauseTrack(APIView):
    def put(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://api.spotify.com/v1/me/player/pause"
        requests.put(url, headers=headers,verify=False)
        return JsonResponse({"message": "Pause du morceau  réussi ✅"}, status=200)


@extend_schema(tags=['SpotifyUserData'])
class SpotifyResumeTrack(APIView):
    def put(self, request):
        user = request.user
        token_helper = SpotifyTokenMixin()
        access_token = token_helper.getValidSpotifyToken(user)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://api.spotify.com/v1/me/player/play"
        requests.put(url, headers=headers,verify=False)
        return JsonResponse({"message": "Reprise du morceau  réussi ✅"}, status=200)


