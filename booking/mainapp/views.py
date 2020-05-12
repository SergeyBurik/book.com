import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse
from mainapp.models import Hotel, Room, Bookings, RoomGallery, Comment, HotelFacility
from mainapp.utils import check_booking, insert_booking, get_coordinates, send_confirmation_mail
from mainapp.variables import at_time


def main_page(request):
    title = 'Home'
    user = request.user

    return render(request, 'mainapp/index.html', {'user': user, 'title': title})


def bookings_main(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id, is_active=True)
    rooms = Room.objects.filter(hotel=hotel, is_active=True)
    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]
    images = RoomGallery.objects.filter(room__hotel=hotel, is_avatar=True)
    coordinates = get_coordinates(hotel.location)
    comments = Comment.objects.filter(hotel__id=hotel_id).order_by('-pub_date')[:5]
    facilities = HotelFacility.objects.filter(hotel__id=hotel.id)
    facility_names = []
    facility_icons = []
    for name in range(len(facilities)):
        facility_names.append(facilities[name].get_name())
        facility_icons.append(facilities[name].get_icon())
    facility_dict = dict(zip(facility_names, facility_icons))

    try:
        rates = Comment.objects.filter(hotel__id=hotel_id)
        rating = [rate.rate for rate in rates]
        rating = sum(rating) / len(rating)
    except ZeroDivisionError:
        rating = 0

    content = {
        'hotel': hotel,
        'rooms': rooms,
        'days': days,
        'coordinates': coordinates,
        'images': images,
        'comments': comments,
        'rating': rating,
        'facilities': facilities,
        'facility_dict': facility_dict,
    }

    return render(request, 'mainapp/booking_main.html', content)


def book_room(request, hotel_id, room_id):
    user = request.user
    hotel = get_object_or_404(Hotel, pk=hotel_id, is_active=True)
    room = get_object_or_404(Room, hotel=hotel, pk=room_id, is_active=True)
    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]
    time = at_time
    total = None
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
            insert_booking(hotel, check_in, check_out, room, '{} {}'.format(client_name, client_surname), email, phone, time,
                           comments, country, address)
            send_confirmation_mail(hotel_id, room_id, check_in, check_out, '{}:{}'.format(client_name, client_surname))
            # ":" is just separator
            return HttpResponseRedirect(reverse('order:pay',
                                                kwargs={
                                                    'hotel_id': hotel_id,
                                                    'room_id': room_id,
                                                    'check_in': check_in,
                                                    'check_out': check_out
                                                }))
        else:
            messages.error(request, 'This room is not available at this period')

    images = RoomGallery.objects.filter(room__hotel=hotel, room=room)
    coordinates = get_coordinates(room.hotel.location)
    print(room.hotel.location)
    print(coordinates)
    content = {
        'user': user,
        'hotel': hotel,
        'room': room,
        'days': days,
        'coordinates': coordinates,
        'summ': total,
        'time': time,
        'images': images
    }
    return render(request, 'mainapp/book_room.html', content)


def total_sum(hotel_id, room_id, check_in, check_out):
    booking = get_object_or_404(Bookings, hotel__pk=hotel_id,
                                hotel__is_active=True, room__pk=room_id,
                                date=check_in)

    start = datetime.datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.datetime.strptime(check_out, "%Y-%m-%d")
    date_list = [start + datetime.timedelta(days=x)
                 for x in range(0, (end - start).days + 1)]
    total = sum([booking.room.price for x in range(len(date_list))])
    return total


def add_comment(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.comment_set.create(author=request.POST['name'],
                             rate=request.POST['stars'],
                             comment=request.POST['text'])

    return HttpResponseRedirect(reverse('main:bookings_main',
                                        args=(hotel.id,)))
