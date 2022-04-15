from django.shortcuts import render
from rest_framework.utils import serializer_helpers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from orders.models import SalesOrder
from products.models import Product
from rest_framework.response import Response
from .serializers import OrderSerializer
from products.serializers import ProductSerializer
from rest_framework.renderers import JSONRenderer


def orders_page(request):
    return render(request, 'index.html', {})

class OrderView(generics.ListAPIView):
    queryset = SalesOrder.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveAPIView):
    queryset = SalesOrder.objects.all()
    serializer_class = OrderSerializer

class OrderAPIView(APIView):
    def get(self, request):
        orders = SalesOrder.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# class AddToOrderView(APIView):
#     def post(self, request):
#         product = ProductIdSerializer(data=request.data, many=False)
#         if product.is_valid():
#             pk = request.data.get('id')
#             prod = Product.objects.filter(id=pk)
#             order = SalesOrder.objects.get(id=3)
#             if prod.count() > 0:
#                 #print(order)
#                 #print(prod[0])
#                 order.products.add(prod[0])
#         else:
#             print('invalid')
#         return Response(status=201)


