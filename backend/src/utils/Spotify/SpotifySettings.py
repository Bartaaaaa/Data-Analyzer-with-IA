import os
import base64

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

AUTH_HEADER = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {AUTH_HEADER}",
    "Content-Type": "application/x-www-form-urlencoded",
}
