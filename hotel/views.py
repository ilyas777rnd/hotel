import os.path
import django_filters
from django.http.response import HttpResponse
from django.utils.encoding import smart_str
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.db import connection
from django.db.models import Q
from rest_framework import permissions
from datetime import datetime, timedelta, date
from openpyxl import Workbook


class GetUserData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        data = Token.objects.filter(key=token).values('user__id', 'user__username', 'user__is_staff')[0]
        return Response(data)


################################################################
class EnqTypeGet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = EquipmentType.objects.all()
    serializer_class = EnqTypeSerializer


class EnqTypeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

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
                return Response({"status": "update"})
        else:
            return Response({"status": "error"})

    def delete(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = EquipmentType.objects.get(id=pk)
        instance.delete()
        return Response(status=201)


################################################################
class RoomTypeGet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomTypeAPI(APIView):
    def post(self, request):
        serializer = RoomTypeSerializer(data=request.data)
        # print(serializer)
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

    def delete(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = RoomType.objects.get(id=pk)
        instance.delete()
        return Response(status=201)


################################################################
class GuestAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get_queryset(self):
        guests = Guest.objects.all()
        if self.request.query_params['name']:
            guests = guests.filter(Q(name__icontains=self.request.query_params['name']) | Q(
                surname__icontains=self.request.query_params['name']))
        if self.request.query_params['passport']:
            guests = guests.filter(Q(pasprot_series__icontains=self.request.query_params['passport']) | Q(
                pasprot_number=self.request.query_params['passport']))
        return guests

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id', None)
            booking_id = request.data.get('booking', None)
            if (pk is None) and not (booking_id is None):
                serializer.save()
                booking = Booking.objects.get(id=booking_id)
                guest = Guest.objects.all().order_by('-id')[0]
                booking.guests.add(guest)
                return Response({"status": "add"})
            else:
                try:
                    guest = Guest.objects.filter(id=pk)
                    guest.update(name=request.data.get('name'), surname=request.data.get('surname'),
                                 pasprot_series=request.data.get('pasprot_series'),
                                 pasprot_number=request.data.get('pasprot_number'),
                                 phone=request.data.get('phone'), email=request.data.get('email'),
                                 birth_date=request.data.get('birth_date'))
                    return Response({"status": "update"})
                except:
                    return Response({"status": "error"})
        else:
            return Response({"status": "error"})

    def delete(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = Guest.objects.get(id=pk)
        instance.delete()
        return Response(status=201)


################################################################


class EquipmentGet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
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

    def delete(self, request):
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
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        room_type = request.GET.get('type', None)
        if not start_date and not end_date:
            rooms = Room.objects.all()
        else:
            bookings = Booking.objects.filter(
                Q(start_date__range=[start_date, end_date]) |
                Q(end_date__range=[start_date, end_date]) |
                Q(end_date__gte=end_date, start_date__lte=start_date))
            rooms = Room.objects.all() \
                .exclude(id__in=[o.room.id for o in bookings])
        if room_type:
            rooms = rooms.filter(type=room_type)
        serializer = RoomViewSerializer(rooms.order_by('number'), many=True)
        return Response(serializer.data)


class RoomAPI(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id')
            serializer.save()
            return Response({"status": "add"})
        else:
            return Response({"status": "error"})

    def patch(self, request):
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

    def delete(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = Room.objects.get(id=pk)
        instance.delete()
        return Response(status=201)


################################################################
class BookingDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingViewSerializer


class BookingAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_report(self, data):

        wb = Workbook()
        ws = wb.active
        ws.append(['Номер брони', 'Дата начала', 'Дата окончания', 'Комната', 'Итого'])
        sum = 0.0
        for item in data:
            sum += float(item['total'])
            ws.append([str(item['id']), item['start_date'], item['end_date'], str(item['room']), str(item['total'])])
        ws.append(['Сумма', str(sum)])
        return wb

    def get(self, request):
        start = self.request.query_params['start_date']
        end = self.request.query_params['end_date']
        room_type = self.request.query_params['room_type']
        room_number = self.request.query_params['room_number']

        start = end if end and not start else start
        end = start if start and not end else end
        if start and end:
            bookings = Booking.objects \
                .filter(Q(start_date__range=[f"{start}", f"{end}"]) |
                        Q(end_date__range=[f"{start}", f"{end}"]) |
                        Q(end_date__gte=end, start_date__lte=start)).order_by('-id')
        else:
            bookings = Booking.objects.none()

        if room_type and bookings:
            bookings = bookings.filter(room__type=room_type)
        if room_number and bookings:
            bookings = bookings.filter(room__id=room_number)
        serializer = BookingViewSerializer(bookings, many=True)

        # self.get_report(serializer.data)

        # wb = self.get_report(serializer.data)
        # wb.save("sample.xlsx")
        # filename = "example.xlsx"

        # response = HttpResponse(content_type='application/ms-excel')
        # response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.xlsx"'
        # wb.save(response)

        # return response
        # file_path = r"C:\Users\sulin\source\repos\Django_mini_course" + f'\{filename}'
        # wb.save(filename)
        # if os.path.exists(file_path):
        #     print('yes')
        #     response = HttpResponse(content_type='application/vnd.ms-excel')
        #     response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        #     return response
        wb = self.get_report(serializer.data)
        wb.save("sample.xlsx")

        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                current_booking = serializer.save()
                if request.data.get('guest[id]'):
                    guest = Guest.objects.get(id=request.data.get('guest[id]'))
                else:
                    guest = Guest(name=request.data.get('guest[name]'), surname=request.data.get('guest[surname]'),
                                  pasprot_series=request.data.get('guest[pasprot_series]'),
                                  pasprot_number=request.data.get('guest[pasprot_number]'),
                                  phone=request.data.get('guest[phone]'), email=request.data.get('guest[email]'),
                                  birth_date=request.data.get('guest[birth_date]'))
                    guest.save()
                current_booking.guests.add(guest)
                return Response({"status": "add", "id": current_booking.id})
            else:
                booking = Booking.objects.filter(id=pk)
                booking.update(room=int(request.data.get('room')), start_date=request.data.get('start_date'),
                               end_date=request.data.get('end_date'), deposit=float(request.data.get('deposit')),
                               total=float(request.data.get('total')),
                               status=request.data.get('status'), manager=int(request.data.get('manager')))
                return Response({"status": "update", "id": pk})
        else:
            return Response({"status": "error"})

    def delete(self, request):
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
class EquipmentListAPI(APIView):
    def get(self, request):
        list = EquipmentList.objects.all()
        serializer = EquipmentListViewSerializer(list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EquipmentListSerializer(data=request.data)
        if serializer.is_valid():
            pk = request.data.get('id')
            if pk is None:
                serializer.save()
                return Response({"status": "add"})
            else:
                instance = EquipmentList.objects.get(id=pk)
                instance.qty = request.data.get('qty')
                instance.save()
                return Response({"status": "update"})
        else:
            return Response({"status": "error"})

    def delete(self, request):
        pk = request.data.get('id')
        if pk is None:
            return Response(status=500)
        instance = EquipmentList.objects.get(id=pk)
        instance.delete()
        return Response(status=201)
