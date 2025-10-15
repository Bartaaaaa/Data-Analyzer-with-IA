from rest_framework import serializers
from ..models.ProductModel import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at'] # Champs à exposer dans l'API