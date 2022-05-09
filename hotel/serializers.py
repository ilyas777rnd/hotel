from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class CurrentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email', 'is_staff']
        # fields = "__all__"


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
    # type = EnqTypeSerializer()
    class Meta:
        model = Equipment
        fields = "__all__"


class EquipmentViewSerializer(ModelSerializer):
    type = SerializerMethodField(read_only=True)
    typeid = SerializerMethodField(read_only=True)

    def get_type(self, obj):
        return obj.type.name

    def get_typeid(self, obj):
        return obj.type.id

    class Meta:
        model = Equipment
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomViewSerializer(ModelSerializer):
    type = SerializerMethodField(read_only=True)
    typeid = SerializerMethodField(read_only=True)

    def get_type(self, obj):
        return obj.type.name

    def get_typeid(self, obj):
        return obj.type.id

    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingViewSerializer(ModelSerializer):
    guests = GuestSerializer(many=True)
    room = SerializerMethodField(read_only=True)
    roomid = SerializerMethodField(read_only=True)
    type = SerializerMethodField(read_only=True)
    dailyprice = SerializerMethodField(read_only=True)
    manager = CurrentUserSerializer()

    def get_room(self, obj):
        return obj.room.number

    def get_roomid(self, obj):
        return obj.room.id

    def get_type(self, obj):
        return obj.room.type.name

    def get_dailyprice(self,obj):
        return obj.room.daily_price

    class Meta:
        model = Booking
        fields = "__all__"


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class EquipmentListViewSerializer(ModelSerializer):
    room = SerializerMethodField(read_only=True)
    enquipment = SerializerMethodField(read_only=True)
    wearout = SerializerMethodField(read_only=True)

    def get_room(self, obj):
        return obj.room.number

    def get_enquipment(self, obj):
        return obj.enquipment.name

    def get_wearout(self, obj):
        return obj.enquipment.wearout

    class Meta:
        model = EquipmentList
        fields = "__all__"


class EquipmentListSerializer(ModelSerializer):
    class Meta:
        model = EquipmentList
        fields = "__all__"
