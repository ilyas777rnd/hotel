from .views import *
from django.urls import path

urlpatterns = [
  path("user_data/", GetUserData.as_view()),
  #EnquipmentType
  path("enq_type_list/", EnqTypeList.as_view()),
  path("enq_type_detail/<int:pk>/", EnqTypeDetailView.as_view()),
  path("enq_type/", EnqTypeAPI.as_view()),
  path("remove_enq_type/", EnqTypeRemove.as_view()),
  #RoomType
  path("room_type_list/", RoomTypeList.as_view()),
  path("room_type_detail/<int:pk>/", RoomTypeDetailView.as_view()),
  path("room_type/", RoomTypeAPI.as_view()),
  path("remove_room_type/", RoomTypeRemove.as_view()),
  #Guest
  path("guest_list/", GuestList.as_view()),
  path("guest_detail/<int:pk>/", GuestDetailView.as_view()),
  path("guest/", GuestAPIView.as_view()),
  path("guest_remove/", GuestRemove.as_view()),
  #Equipment
  path("equipment_view/", EquipmentView.as_view()),
  path("equipment_detail/<int:pk>/", EquipmentDetailView.as_view()),
  path("equipment/", EquipmentAPI.as_view()),
  path("equipment_remove/", EquipmentRemove.as_view()),
  #Room
  path("room_view/", RoomView.as_view()),
  path("room_detail/<int:pk>/", RoomDetailView.as_view()),
  path("room/", RoomAPI.as_view()),
  path("room_upd/", RoomUpdate.as_view()),
  path("room_remove/", RoomRemove.as_view()),
  #Booking
  path("booking_view/", BookingView.as_view()),
  path("booking_detail/<int:pk>/", BookingDetailView.as_view()),
  path("last_booking/", LastBooking.as_view()),
  path("booking/", BookingAPI.as_view()),
  path("booking_remove/", BookingRemove.as_view()),
  path("booking_add_guest/", BookingAddGuest.as_view()),
  path("booking_remove_guest/", BookingRemoveGuest.as_view()),
  #EquipmentList
  path("enq_list_view/", EquipmentListView.as_view()),
  path("enq_list/", EquipmentListAPI.as_view()),
  path("enq_list_remove/", EquipmentListRemove.as_view()),
]