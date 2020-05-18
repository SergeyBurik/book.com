# coding: utf-8
from django.urls import path
from apiapp import views as apiapp

app_name = 'apiapp'


urlpatterns = [
    path('getRooms/', apiapp.get_rooms, name='get_rooms'),
    path('getHotel/', apiapp.get_hotel, name='get_hotel'),
    path('getRoom/', apiapp.get_room, name='get_room'),
    path('getRoomBookings/', apiapp.get_bookings, name='get_bookings'),
    path('getHotelBookings/', apiapp.get_hotel_bookings, name='get_hotel_bookings'),
    path('createBooking/', apiapp.create_booking, name='create_booking'),
    path('getImages/', apiapp.get_hotel_images, name='get_hotel_images'),
    path('getRatings/', apiapp.get_ratings, name='get_ratings'),
    path('filterRooms/', apiapp.filter_rooms, name='filter_rooms'),
    path('addRating/', apiapp.add_rating, name='add_rating'),
]
