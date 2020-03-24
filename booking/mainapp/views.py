import datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from mainapp.models import Hotel, Room

from mainapp.utils import check_booking, insert_booking


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

    if request.method == 'POST':
        check_in = request.POST.get('start', None)
        check_out = request.POST.get('end', None)
        client_name = request.POST.get('client_name', None)
        client_surname = request.POST.get('client_surname', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        time = request.POST.get('time', None)
        comments = request.POST.get('comments', None)
        country = request.POST.get('country', None)
        address = request.POST.get('address', None)
        print(check_in, check_out, client_name, client_surname, email, phone, time, comments, country, address)

        if check_booking(check_in, check_out, room_id, hotel_id):  # if there are not any reservations
            insert_booking(hotel, check_in, check_out, room, f'{client_name} {client_surname}', email, phone, time,
                           comments,
                           country, address)

            messages.success(request, 'You successfully booked room!')
        else:
            messages.error(request, 'This room is not available at this period')

    return render(request, 'mainapp/book_room.html', {'user': user,
                                                      'hotel': hotel,
                                                      'room': room,
                                                      'days': days,
                                                      })
