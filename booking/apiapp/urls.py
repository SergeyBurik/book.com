# coding: utf-8
from django.urls import path
from apiapp import views as apiapp

app_name = 'apiapp'

urlpatterns = [
    path('getRooms/', apiapp.get_rooms, name='get_rooms'),
    path('getHotel/', apiapp.get_hotel, name='get_hotel'),
    path('getRoom/', apiapp.get_room, name='get_room'),
    path('createBooking/', apiapp.create_booking, name='create_booking'),
]
