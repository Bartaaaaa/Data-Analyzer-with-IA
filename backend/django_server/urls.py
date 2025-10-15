from django.contrib import admin
from django.urls import path, include  # Assurez-vous d'importer 'include'
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # La seule ligne nécessaire pour connecter votre application API
    path('src/v1/', include('src.urls.ProductUrl')),
    path('src/v1/', include('src.urls.UserUrl')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-token-auth/', views.obtain_auth_token)
]