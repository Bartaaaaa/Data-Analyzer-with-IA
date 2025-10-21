from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('django.contrib.auth.urls')),
    path('api/login', views.obtain_auth_token),

    path('api/', include('src.urls.ProductUrl')),
    # USER RELATED PATH #
    path('api/', include('src.urls.UserUrl')),

    # SPOTIFY RELATED PATH #
    path('api/', include('src.urls.SpotifyTokenUrl')),

]