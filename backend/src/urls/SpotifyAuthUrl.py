from django.urls import path
from src.views.SpotifyAuthView import (
    SpotifyLoginView,
    SpotifyCallbackView,
    SpotifyCheckTokenView
)

urlpatterns = [
    path("login", SpotifyLoginView.as_view(), name="spotify-login"),
    path("callback", SpotifyCallbackView.as_view(), name="spotify-callback"),
    path("checkToken", SpotifyCheckTokenView.as_view(), name="spotify-checkToken"),
]
