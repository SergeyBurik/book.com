import datetime

from django.shortcuts import get_object_or_404
from geopy.geocoders import Nominatim
from mainapp.models import Bookings, Room, Hotel


# returns coordinates by address
def get_coordinates(address):
    try:
        geolocator = Nominatim(user_agent="get_coordinates")
        location = geolocator.geocode(address)
        return (round(location.latitude, 6), round(location.longitude, 6))

    except AttributeError:
        return (0, 0)


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
    date_list = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]

    for date in date_list:
        Bookings.objects.create(hotel=hotel,
                                date=date,
                                room=room,
                                client_name=client_name,
                                client_email=client_email,
                                phone_number=phone_number,
                                time=time,
                                comments=comments,
                                country=country,
                                address=address)
