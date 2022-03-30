from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class CurrentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email', 'is_staff']
        #fields = "__all__"

class EnqTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = "__all__"

class RoomTypeSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"

class GuestSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"

class EquipmentSerializer(ModelSerializer):
    #type = EnqTypeSerializer()
    class Meta:
        model = Equipment
        fields = "__all__"

class EquipmentViewSerializer(ModelSerializer):
    type = EnqTypeSerializer()
    class Meta:
        model = Equipment
        fields = "__all__"

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class RoomViewSerializer(ModelSerializer):
    type = RoomTypeSerializer()
    class Meta:
        model = Room
        fields = "__all__"

class BookingSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class BookingViewSerializer(ModelSerializer):
    guests = GuestSerializer(many=True)
    room = RoomSerializer()
    manager = CurrentUserSerializer()
    class Meta:
        model = Booking
        fields = "__all__"

class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class EquipmentListViewSerializer(ModelSerializer):
    room = RoomSerializer()
    enquipment = EquipmentSerializer()
    class Meta:
        model = EquipmentList
        fields = "__all__"

class EquipmentListSerializer(ModelSerializer):
    class Meta:
        model = EquipmentList
        fields = "__all__"