import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from mainapp.models import Hotel, Room, Bookings, RoomGallery, Comment, HotelFacility
from mainapp.utils import check_booking, insert_booking, get_coordinates, send_confirmation_mail
from mainapp.variables import at_time
from django.urls import reverse
from mainapp.models import Hotel, Room, Bookings, RoomGallery, Comment
from mainapp.utils import check_booking, insert_booking, get_coordinates, send_confirmation_mail, create_room_booking

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
        success = create_room_booking(request, room_id, hotel_id)

    images = RoomGallery.objects.filter(room__hotel=hotel, room=room)
    coordinates = get_coordinates(room.hotel.location)

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
    total = sum([booking.room.price for x in range(len(date_list)-1)])
    return total


def add_comment(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.comment_set.create(author=request.POST['name'],
                             rate=request.POST['stars'],
                             comment=request.POST['text'])

    return HttpResponseRedirect(reverse('main:bookings_main',
                                        args=(hotel.id,)))
