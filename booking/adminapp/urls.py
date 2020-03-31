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

    # ajax
    path('ajax/check_address/', adminapp.ajax_check_address, name="ajax_check_address"),

]
