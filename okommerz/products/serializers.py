from rest_framework import routers, serializers, viewsets
from .models import ProductItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ['product_name', 'product_category', 'description', 'amount', 'regular_price', 'sales_price', 'product_image', 'additional_detail']

