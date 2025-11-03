# src/urls/user_urls.py
from django.urls import path
from ..views.AuthView import UserRegister
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema, extend_schema_view
urlpatterns = [
    path('register', UserRegister.as_view(), name='user-register'),
    path('login',
         extend_schema_view(
             post=extend_schema(
                 summary="1. Obtenir un token JWT (Login)",
                 description="Fournissez un nom d'utilisateur et un mot de passe pour obtenir un token d'accès et un token de rafraîchissement.",
                 tags=['Auth']
             )
         )(TokenObtainPairView.as_view()),
         name='token_obtain_pair'),
    path('token/refresh',
         extend_schema_view(
             post=extend_schema(
                 summary="2. Rafraîchir un token JWT",
                 description="Fournissez un token de rafraîchissement (refresh token) valide pour obtenir un nouveau token d'accès.",
                 tags=['Auth']
             )
         )(TokenRefreshView.as_view()),
         name='token_refresh'),
]