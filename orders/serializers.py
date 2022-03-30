from rest_framework.serializers import ModelSerializer
from .models import SalesOrder
from  products.models import Product
from products.serializers import ProductSerializer,ProductIdSerializer
from rest_framework import generics


# class OrderSerializer(ModelSerializer):
#     class Meta:
#         model = SalesOrder
#         fields = ['amount', 'description']

class OrderSerializer(ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = SalesOrder
        fields = ['amount', 'description','products']

        
