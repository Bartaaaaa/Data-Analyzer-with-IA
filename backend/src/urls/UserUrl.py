from django.urls import path
from ..views.UserView import CurrentUserView

urlpatterns = [
    path('users/me/', CurrentUserView.as_view(), name='user-me'),
]