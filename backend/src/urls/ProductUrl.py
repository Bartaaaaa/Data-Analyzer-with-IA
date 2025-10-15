from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.ProductView import ProductViewSet

# Crée un routeur pour gérer les routes de l'API
router = DefaultRouter()

# Enregistre la route 'products' pour qu'elle pointe vers le ProductViewSet
router.register(r'products', ProductViewSet, basename='product')

# On expose uniquement les URLs générées par le routeur
urlpatterns = [
    path('', include(router.urls)),
]