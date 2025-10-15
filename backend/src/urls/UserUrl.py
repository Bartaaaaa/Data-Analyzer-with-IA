# src/urls/user_urls.py
from django.urls import path
from ..views.UserView import UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
]