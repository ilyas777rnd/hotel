from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'enq_type_get', EnqTypeGet, basename='enq_type')
router.register(r'room_type_get', RoomTypeGet, basename='room_type')
router.register(r'equipment_get', EquipmentGet, basename='equipment')
urlpatterns = router.urls

urlpatterns += [
    path("user_data/", GetUserData.as_view()),
    # EnquipmentType
    path("enq_type/", EnqTypeAPI.as_view()),
    # RoomType
    path("room_type/", RoomTypeAPI.as_view()),
    # Guest
    path("guest/", GuestAPIView.as_view()),
    # Equipment
    path("equipment/", EquipmentAPI.as_view()),
    # Room
    path("room_view/", RoomView.as_view()),
    path("room/", RoomAPI.as_view()),
    # Booking
    path("booking_detail/<int:pk>/", BookingDetailView.as_view()),
    path("booking/", BookingAPI.as_view()),
    path("booking_report/", report_view),
    path("booking_add_guest/", BookingAddGuest.as_view()),
    path("booking_remove_guest/", BookingRemoveGuest.as_view()),
    # EquipmentList
    path("eq_list/", EquipmentListAPI.as_view()),
    # Report
    path("report/", ReportView.as_view())
]
