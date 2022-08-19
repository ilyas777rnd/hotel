import os.path
import calendar
from django.db.models.aggregates import Sum
from django.http import HttpResponse
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


def get_booking_report(data):
    wb = Workbook()
    ws = wb.active
    ws.append(['Номер брони', 'Дата начала', 'Дата окончания', 'Комната', 'Статус', 'Депозит', 'Итого'])
    sum = 0.0
    for item in data:
        if item['status'] == 'Забронирован':
            sum += float(item['deposit'])
        else:
            sum += float(item['total'])
        ws.append(
            [str(item['id']), item['start_date'], item['end_date'], str(item['room']), str(item['status']),
             str(item['deposit']), str(item['total'])])
    ws.append(['Сумма', str(sum)])
    return wb


def found_bookings(start, end, room_type, room_number, guest, status):
    start = end if end and not start else start
    end = start if start and not end else end
    if start and end:
        bookings = Booking.objects \
            .filter(Q(start_date__range=[f"{start}", f"{end}"]) |
                    Q(end_date__range=[f"{start}", f"{end}"]) |
                    Q(end_date__gte=end, start_date__lte=start)).order_by('-id')
        if guest:
            bookings = bookings.filter(guests__name__icontains=guest)
        if status:
            bookings = bookings.filter(status=status)
    else:
        bookings = Booking.objects.none()
    if room_type and bookings:
        bookings = bookings.filter(room__type=room_type)
    if room_number and bookings:
        bookings = bookings.filter(room__id=room_number)
    return bookings


def report_view(request):
    start = request.GET['start_date']
    end = request.GET['end_date']
    room_type = request.GET['room_type']
    room_number = request.GET['room_number']
    guest = request.GET['guest']
    status = request.GET['status']
    bookings = found_bookings(start, end, room_type, room_number, guest, status)
    data = BookingViewSerializer(bookings, many=True).data
    wb = get_booking_report(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report.xlsx"'
    wb.save(response)
    return response


class GetUserData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        data = Token.objects.filter(key=token).values('user__id', 'user__username', 'user__is_staff')[0]
        return Response(data)


################################################################
class EnqTypeGet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = EquipmentType.objects.all()
    serializer_class = EnqTypeSerializer


class EnqTypeAPI(APIView):
    permission_classes = [permissions.IsAdminUser, ]

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
    permission_classes = [permissions.IsAdminUser, ]

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


################################################################


class EquipmentGet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Equipment.objects.all()
    serializer_class = EquipmentViewSerializer


class EquipmentAPI(APIView):
    permission_classes = [permissions.IsAdminUser, ]

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
        start_date_str = request.GET.get('start_date', None)
        end_date_str = request.GET.get('end_date', None)
        room_type = request.GET.get('type', None)
        if not start_date_str and not end_date_str:
            rooms = Room.objects.all()
        else:
            start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if timedelta(1) == (end - start):
                bookings = Booking.objects.filter(end_date__gte=end, start_date__lte=start)
            else:
                bookings = found_bookings(start + timedelta(1), end - timedelta(1), None, None, None, None)
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
            room = Room.objects.filter(id=pk)
            room.update(number=request.data.get('number'), rooms_qty=int(request.data.get('rooms_qty')),
                        sleeper_qty=int(request.data.get('sleeper_qty')),
                        daily_price=float(request.data.get('daily_price')),
                        type=RoomType.objects.get(id=request.data.get('type')))
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

    def get(self, request):
        start = self.request.query_params['start_date']
        end = self.request.query_params['end_date']
        room_type = self.request.query_params['room_type']
        room_number = self.request.query_params['room_number']
        guest = self.request.query_params['guest']
        status = self.request.query_params['status']
        bookings = found_bookings(start, end, room_type, room_number, guest, status)
        serializer = BookingViewSerializer(bookings, many=True)

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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        guest = Guest.objects.get(id=request.data.get('guest'))
        booking = Booking.objects.get(id=request.data.get('booking'))
        booking.guests.add(guest)
        return Response({"status": "add"})


class BookingRemoveGuest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        guest = Guest.objects.get(id=request.data.get('guest'))
        booking = Booking.objects.get(id=request.data.get('booking'))
        booking.guests.remove(guest)
        return Response({"status": "remove"})


################################################################
class EquipmentListAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

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


class ReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def found_rooms(self, type, capacity):
        rooms = Room.objects.all()
        if type:
            rooms = rooms.filter(type=type)
        if capacity:
            rooms = rooms.filter(sleeper_qty=int(capacity)) if int(capacity) < 4 else rooms.filter(sleeper_qty__gte=4)
        return rooms

    def monthly_report(self, month, type, capacity):
        result = {}
        month_split = month.split('-')
        first_day_of_month = date(int(month_split[0]), int(month_split[1]), 1)
        last_day_of_month = date(int(month_split[0]), int(month_split[1]),
                                 calendar.monthrange(int(month_split[0]), int(month_split[1]))[1])
        all_bookings_in_this_month = found_bookings(first_day_of_month, last_day_of_month, type, None, None, None)
        rooms = self.found_rooms(type, capacity)
        booked_rooms = rooms.filter(id__in=[o.room.id for o in all_bookings_in_this_month])
        result['busy_percent'] = (float(len(booked_rooms)) / float(len(rooms))) * 100.0
        start_bookings_in_this_month = Booking.objects\
            .filter(start_date__range=[first_day_of_month, last_day_of_month])
        result['sum'] = start_bookings_in_this_month.aggregate(Sum('total'))
        return result

    def daily_report(self, date, type, capacity):
        result = {}
        all_bookings_in_this_day = found_bookings(date, date, type, None, None, None)
        rooms = self.found_rooms(type, capacity)
        booked_rooms = rooms.filter(id__in=[o.room.id for o in all_bookings_in_this_day])
        result['busy_percent'] = (float(len(booked_rooms)) / float(len(rooms))) * 100.0

        start_bookings_in_this_day = Booking.objects.filter(start_date=date)
        result['sum'] = start_bookings_in_this_day.aggregate(Sum('total'))
        return result

    def get(self, request):
        start = datetime.strptime(self.request.query_params['start_date'], "%Y-%m-%d").date()
        end = datetime.strptime(self.request.query_params['end_date'], "%Y-%m-%d").date() + timedelta(1)
        room_type = self.request.query_params['room_type']
        capacity = self.request.query_params['capacity']
        period = self.request.query_params['period']
        result = {}

        if period == 'daily':
            date_generated = [start + timedelta(x) for x in range(0, (end - start).days)]
            for day in date_generated:
                result[day.isoformat()] = self.daily_report(day, room_type, capacity)
        elif period == 'monthly':
            date_generated = [start + timedelta(x) for x in range(0, (end - start).days)]
            month_set = set()
            for day in date_generated:
                month_set.add(day.strftime('%Y-%m'))
            for month in sorted(month_set):
                result[month] = self.monthly_report(month, room_type, capacity)
        else:
            pass
        print(result)
        return Response(result)
