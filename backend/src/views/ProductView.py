# src/views.py

from rest_framework import viewsets
from ..models.ProductModel import Product
from ..serializers.ProductSerializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer