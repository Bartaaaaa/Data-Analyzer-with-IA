# src/views/user_views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..serializers.UserSerializer import UserSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Auth'])
class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

