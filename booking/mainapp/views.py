import datetime

from django.shortcuts import render, get_object_or_404
from mainapp.models import Hotel, Room


def main_page(request):
    user = request.user

    return render(request, 'mainapp/index.html', {'user': user})


def bookings_main(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, is_active=True)
    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]

    return render(request, 'mainapp/booking_main.html', {'hotel': hotel,
                                                         'rooms': rooms,
                                                         'days': days})


def book_room(request, hotel_id, room_id):
    user = request.user
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(Room, hotel=hotel, pk=room_id, is_active=True)
    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]

    return render(request, 'mainapp/book_room.html', {'user': user,
                                                      'hotel': hotel,
                                                      'room': room,
                                                      'days': days})
