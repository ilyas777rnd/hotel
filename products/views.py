from django.shortcuts import render
from rest_framework.utils import serializer_helpers
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework import permissions
from django.contrib.admin.views.decorators import staff_member_required

class ProductsListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        if self.request.user.is_staff:
            products = Product.objects.all()
            return products
        else:
            return None
