from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from .models import Product
from rest_framework import generics

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ProductIdSerializer(Serializer):
    class Meta:
        model = Product
        fields = ['id']

class ProductFields(Serializer):
    class Meta:
        model = Product
        fields = ['id','amount']
