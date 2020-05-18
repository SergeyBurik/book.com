import datetime

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from geopy.geocoders import Nominatim
from mainapp.models import Bookings, Room, Hotel
from django.conf import settings
import geopy
# returns coordinates by address
from ordersapp.models import Order


def get_coordinates(address):
    try:
        geolocator = Nominatim(user_agent="get_coordinates")
        location = geolocator.geocode(address)
        return (round(location.latitude, 6), round(location.longitude, 6))
    except AttributeError:
        return (0, 0)
    except geopy.exc.GeocoderTimedOut:
        return (0, 0)


def send_confirmation_mail(hotel_id, room_id, check_in, check_out, client_name):
    print('send_confirmation_mail')
    booking = get_object_or_404(Bookings, hotel__pk=hotel_id, room__pk=room_id, date=check_in)
    start = datetime.datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.datetime.strptime(check_out, "%Y-%m-%d")
    date_list = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]

    total = sum([booking.room.price for x in range(len(date_list))])

    data = {'booking': booking, 'nights': len(date_list), 'first_name': booking.client_name.split(':')[0],
            'check_in': check_in, 'check_out': check_out, 'total': total, 'domain': settings.DOMAIN_NAME,
            'coordinates': str(get_coordinates(booking.hotel.location))}
    print(data)

    html_m = render_to_string('mainapp/confirmation_letter.html', data)

    return send_mail('Booking Confirmation', '', settings.EMAIL_HOST_USER,
                     [booking.client_email], html_message=html_m, fail_silently=False)


# function which checks availability of room for selected dates
def check_booking(date_from, date_to, room_id, hotel_id):
    """

    :param date_from:
    :param date_to:
    :param room_id:
    :param hotel_id:
    :return:
    """
    start = datetime.datetime.strptime(date_from, "%Y-%m-%d")
    end = datetime.datetime.strptime(date_to, "%Y-%m-%d")
    date_list = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]  # list of dates
    hotel = get_object_or_404(Hotel, pk=hotel_id, is_active=True)
    room = get_object_or_404(Room, pk=room_id, hotel=hotel, is_active=True)

    # if the first date element is earlier than today: return False
    if str(date_list[0]).split(' ')[0] < str(datetime.datetime.today()).split(' ')[0]:
        return False
    # else: check for every day
    for date in date_list:
        # if booking for this room, at this hotel, and for this date exists: return False
        #  select * from `table` where room = room and date = date and hotel = hotel
        if len(Bookings.objects.filter(room=room, room__is_active=True, hotel=hotel, date=str(date).split(' ')[0])):
            return False
        else:
            continue

    return True


# function which creates booking records
def insert_booking(hotel, check_in, check_out, room, client_name, client_email, phone_number, time, comments, country,
                   address):
    """
    :param hotel: Hotel instance
    :param check_in: datetime
    :param check_out: datetime
    :param room: Room instance
    :param client_name: client_name + client_surname
    :param client_email: client's email
    :param phone_number: client's phone number
    :param time: estimated time of arrival
    :param comments: client's comments
    :param country: client's country
    :param address: client's address
    :return:
    """
    start = datetime.datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.datetime.strptime(check_out, "%Y-%m-%d")
    # dates list
    date_list = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    days_quantity = len(date_list)
    total_sum = room.price * days_quantity
    # total_ = sum([booking.room.price for x in range(len(date_list))])
    for date in date_list:
        booking = Bookings.objects.create(hotel=hotel,
                                          date=date,
                                          room=room,
                                          client_name=client_name,
                                          client_email=client_email,
                                          phone_number=phone_number,
                                          time=time,
                                          comments=comments,
                                          country=country,
                                          address=address)

    create_order(client_name, client_email, days_quantity, total_sum, booking)


def create_order(name, email, quantity, total, booking):
    Order.objects.create(client_name=name,
                         client_email=email,
                         days=quantity,
                         booking=booking,
                         total_sum=total)

def create_room_booking(request, room_id, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    room = Room.objects.get(id=room_id)
    print(request)
    print(request.POST)
    if request.method == 'POST':
        check_in = request.POST.get('check_in', None)
        check_out = request.POST.get('check_out', None)
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
            send_confirmation_mail(hotel_id, room_id, check_in, check_out, f'{client_name}:{client_surname}')
            # ":" is just separator
            messages.success(request, f"You successfully booked room from {check_in} to {check_out}")
        else:
            messages.error(request, 'This room is not available at this period')