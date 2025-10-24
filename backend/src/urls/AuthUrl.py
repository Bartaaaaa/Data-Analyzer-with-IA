# src/urls/user_urls.py
from django.urls import path
from ..views.UserView import UserCreateView
from rest_framework.authtoken import views

urlpatterns = [
    path('register', UserCreateView.as_view(), name='user-register'),
    path('login', views.obtain_auth_token),

]