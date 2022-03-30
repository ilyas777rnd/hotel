from orders.views import *
from django.urls import path

urlpatterns = [
    path("orders_detail/<int:pk>/", OrderDetailView.as_view()),
    path("orders/", OrderView.as_view()),
]