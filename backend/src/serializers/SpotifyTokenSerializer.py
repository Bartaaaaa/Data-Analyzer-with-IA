from django.contrib.auth.models import User
from ..models.SpotifyTokenModel import SpotifyToken

from rest_framework import serializers

class SpotifyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyToken
        fields = ['user',  'access_token', 'refresh_token', 'expires_at']

    def create(self, validated_data):
        spotifyToken = SpotifyToken.objects.create_SpotifyToken(
            user=validated_data['user'],
            access_token=validated_data['access_token'],
            refresh_token=validated_data['refresh_token'],
            expires_at=validated_data['expires_at']
        )
        return spotifyToken