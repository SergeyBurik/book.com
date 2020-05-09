from django.urls import path
from adminapp import views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('main/', adminapp.main, name='main'),
    path('create_hotel/', adminapp.create_hotel, name='create_hotel'),
    path('create_room/', adminapp.create_room, name='create_room'),
    path('hotels/', adminapp.hotels, name='hotels'),
    path('rooms/', adminapp.rooms, name='rooms'),
    path('hotel-<int:pk>/edit_hotel/', adminapp.edit_hotel, name="edit_hotel"),
    path('hotel-<int:hotel_id>/room-<int:room_id>/edit_room/', adminapp.edit_room, name="edit_room"),
    path('room-<int:id>/delete/', adminapp.delete_room, name="delete_room"),
    path('hotel-<int:id>/delete/', adminapp.delete_hotel, name="delete_hotel"),
    # ajax
    path('ajax/check_address/', adminapp.ajax_check_address, name="ajax_check_address"),
    path('ajax/delete_image/', adminapp.ajax_delete_image, name="ajax_delete_image"),
    path('ajax/get_rooms/', adminapp.ajax_get_rooms, name="ajax_get_rooms"),

]
