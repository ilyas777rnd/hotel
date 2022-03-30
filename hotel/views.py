from rest_framework.utils import serializer_helpers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from .models import *
from .serializers import *
from django.db import connection
from rest_framework import permissions
from datetime import datetime, timedelta, date

class GetUserData(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        cursor = connection.cursor()
        token = request.headers['Authorization'].split(' ')[1]
        #print(request.data)
        cursor.execute(
            ''' SELECT user_id, username, is_staff FROM authtoken_token JOIN auth_user ON user_id=id WHERE key='{}' 
            '''.format(token))
        row = cursor.fetchone()
        return Response({"user_id":row[0], "username":row[1], "is_staff":row[2]})

class EnqTypeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = EquipmentType.objects.all()
    serializer_class = EnqTypeSerializer

class EnqTypeDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EquipmentType.objects.all()
    serializer_class = EnqTypeSerializer

class EnqTypeAPI(APIView):
    def post(self, request):
        serializer = EnqTypeSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                instance = EquipmentType.objects.get(id=pk)
                instance.name = request.data.get('name')
                instance.save()
                return Response({"status":"update"})
        else:
            return Response({"status": "error"})


class EnqTypeRemove(APIView):
    def post(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = EquipmentType.objects.get(id=pk)
        instance.delete()
        return Response(status=201)
################################################################


class RoomTypeList(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class RoomTypeDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class RoomTypeAPI(APIView):
    def post(self, request):
        serializer = RoomTypeSerializer(data=request.data)
        #print(serializer)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                instance = RoomType.objects.get(id=pk)
                instance.name = request.data.get('name')
                instance.save()
                return Response({"status": "update"})
        else:
            return Response({"status": "error"})

class RoomTypeRemove(APIView):
    def post(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = RoomType.objects.get(id=pk)
        instance.delete()
        return Response(status=201)
################################################################


class GuestList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        name = request.data.get('name',None)
        surname = request.data.get('surname',None)
        guests = Guest.objects.all()
        if not (name is None):
            guests = guests.filter(name__icontains=name)
        if not (surname is None):
            guests = guests.filter(surname__icontains=surname)
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

class GuestDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class GuestAPIView(APIView):
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            print('valid')
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                try:
                    instance = Guest.objects.get(id=pk)
                    instance.name = request.data.get('name')
                    instance.surname = request.data.get('surname')
                    instance.pasprot_series = request.data.get('pasprot_series')
                    instance.pasprot_number = request.data.get('pasprot_number')
                    instance.phone = request.data.get('phone')
                    instance.email = request.data.get('email')
                    instance.birth_date = request.data.get('birth_date')
                    instance.save()
                    return Response({"status": "update"})
                except:
                    return Response({"status": "error"})
        else:
            return Response({"status": "error"})

class GuestRemove(APIView):
    def post(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = Guest.objects.get(id=pk)
        instance.delete()
        return Response(status=201)
################################################################

class EquipmentView(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentViewSerializer

class EquipmentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Equipment.objects.all()
    serializer_class = EquipmentViewSerializer

class EquipmentAPI(APIView):
    def post(self, request):
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                instance = Equipment.objects.get(id=pk)
                instance.name = request.data.get('name')
                instance.type = EquipmentType.objects.get(id=request.data.get('type'))
                instance.wearout = request.data.get('wearout')
                instance.save()
                return Response({"status": "update"})
        else:
            return Response({"status": "error"})

class EquipmentRemove(APIView):
    def post(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = Equipment.objects.get(id=pk)
        instance.delete()
        return Response(status=201)
################################################################

class RoomView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        list = None
        if (request.GET['start_date'] is '') and (request.GET['end_date'] is ''):
            list = Room.objects.all()
        else:
            start = [int(x) for x in request.GET['start_date'].split('-')]
            end = [int(x) for x in request.GET['end_date'].split('-')]
            start_date = date(start[0], start[1], start[2])
            end_date = date(end[0], end[1], end[2])
            print(start_date)
            print(end_date)
            bookings1 = Booking.objects.filter(start_date__range=[start_date, end_date])
            bookings2 = Booking.objects.filter(end_date__range=[start_date, end_date])
            list = Room.objects.all() \
                .exclude(id__in=[o.room.id for o in bookings1]) \
                .exclude(id__in=[o.room.id for o in bookings2]). \
                order_by('number')
        serializer = RoomViewSerializer(list, many=True)
        return Response(serializer.data)

class RoomDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomViewSerializer

class RoomAPI(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                instance = Room.objects.get(id=pk)
                instance.number = request.data.get('number')
                instance.status = request.data.get('status')
                instance.rooms_qty = request.data.get('rooms_qty')
                instance.sleeper_qty = request.data.get('sleeper_qty')
                instance.daily_price = request.data.get('daily_price')
                instance.type = RoomType.objects.get(id=request.data.get('type'))
                instance.save()
                return Response({"status": "update"})
        else:
            return Response({"status": "error"})

class RoomUpdate(APIView):
    def post(self, request):
        try:
            pk = request.data.get('id')
            if pk is None:
                return Response({"status": "error"})
            instance = Room.objects.get(id=pk)
            instance.number = request.data.get('number')
            instance.status = request.data.get('status')
            instance.rooms_qty = request.data.get('rooms_qty')
            instance.sleeper_qty = request.data.get('sleeper_qty')
            instance.daily_price = request.data.get('daily_price')
            instance.type = RoomType.objects.get(id=request.data.get('type'))
            instance.save()
            return Response({"status": "update"})
        except:
            return Response({"status": "error"})


class RoomRemove(APIView):
    def post(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = Room.objects.get(id=pk)
        instance.delete()
        return Response(status=201)
################################################################

class BookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        start = request.GET['start_date']
        end = request.GET['end_date']
        bookings = Booking.objects\
            .filter(start_date__range=[f"{start}", f"{end}"],end_date__range=[f"{start}", f"{end}"])\
            .order_by('-id')
        serializer = BookingViewSerializer(bookings, many=True)
        return Response(serializer.data)

class BookingDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingViewSerializer

class LastBooking(APIView):
    def post(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        cursor = connection.cursor()
        cursor.execute(
            ''' 
            SELECT MAX(id) FROM hotel_booking JOIN authtoken_token ON manager_id=user_id
            WHERE key='{}' 
            '''.format(token))
        row = cursor.fetchone()
        print(row)
        return Response({"id": row[0]})


class BookingAPI(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                instance = Booking.objects.get(id=pk)
                instance.room = Room.objects.get(id=request.data.get('room'))
                instance.start_date = request.data.get('start_date')
                instance.end_date = request.data.get('end_date')
                instance.deposit = request.data.get('deposit')
                instance.total = request.data.get('total')
                instance.status = request.data.get('status')

                instance.save()
                return Response({"status": "update"})
        else:
            return Response({"status": "error"})

class BookingRemove(APIView):
    def post(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = Booking.objects.get(id=pk)
        instance.delete()
        return Response(status=201)

class BookingAddGuest(APIView):
    def post(self, request):
        guest = Guest.objects.get(id=request.data.get('guest'))
        booking = Booking.objects.get(id=request.data.get('booking'))
        booking.guests.add(guest)
        return Response({"status": "add"})

class BookingRemoveGuest(APIView):
    def post(self, request):
        guest = Guest.objects.get(id=request.data.get('guest'))
        booking = Booking.objects.get(id=request.data.get('booking'))
        booking.guests.remove(guest)
        return Response({"status": "remove"})
################################################################
class EquipmentListView(APIView):
    def get(self, request):
        list = EquipmentList.objects.all()
        serializer = EquipmentListViewSerializer(list, many=True)
        return Response(serializer.data)

class EquipmentListAPI(APIView):
    def post(self, request):
        serializer = EquipmentListSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                instance = EquipmentList.objects.get(id=pk)
                #instance.room = Room.objects.get(id=request.data.get('room'))
                #instance.enquipment = Equipment.objects.get(id=request.data.get('enquipment'))
                instance.qty = request.data.get('qty')
                instance.save()
                return Response({"status": "update"})
        else:
            return Response({"status": "error"})

class EquipmentListRemove(APIView):
    def post(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = EquipmentList.objects.get(id=pk)
        instance.delete()
        return Response(status=201)
