import datetime
import json

from django.http import JsonResponse
# Create your views here.
from mainapp.models import Room, Hotel, Bookings, RoomGallery, Comment


def get_rooms(request):
    hotel_id = request.GET['hotel']
    if hotel_id:
        if isinstance(hotel_id, str):
            response = []  # list of rooms
            rooms = Room.objects.filter(hotel__pk=hotel_id, is_active=True)
            for room in rooms:
                images = RoomGallery.objects.filter(room=room)

                response.append({
                    "id": room.id,
                    "hotel": room.hotel.name,
                    "hotel_id": room.hotel.id,
                    "name": room.name,
                    "price": room.price,
                    "description": room.description,
                    "adult": room.adult,
                    "kids": room.kids,
                    "infants": room.infants,
                    "is_active": room.is_active,
                    "images": [
                        {"path": image.image.url} for image in images
                    ]
                })

            return JsonResponse(response, safe=False)

    return JsonResponse({"error": "You should provide hotel id"})


def get_hotel(request):
    hotel_id = request.GET['hotel']
    if hotel_id:
        if isinstance(hotel_id, str):
            try:
                rates = Comment.objects.filter(hotel__id=hotel_id)
                rating = [rate.rate for rate in rates]
                rating = sum(rating) / len(rating)
            except ZeroDivisionError:
                rating = 0

            hotel = Hotel.objects.filter(id=hotel_id, is_active=True)[0]
            response = {
                "id": hotel.id,
                "user": f'{hotel.user.name} {hotel.user.surname}',
                "name": hotel.name,
                "rating": rating,
                "phone_number": hotel.phone_number,
                "location": hotel.location,
                "description": hotel.description,
                "stars": hotel.stars,
                "banner": hotel.banner.url,
            }

            return JsonResponse(response, safe=False)

    return JsonResponse({"error": "You should provide hotel id"}, safe=False)


def get_room(request):
    room_id = request.GET['room']
    if room_id:
        if isinstance(room_id, str):
            room = Room.objects.filter(pk=room_id, is_active=True)[0]
            images = RoomGallery.objects.filter(room=room)

            response = {
                "id": room.id,
                "hotel": room.hotel.name,
                "hotel_id": room.hotel.id,
                "name": room.name,
                "price": room.price,
                "description": room.description,
                "adult": room.adult,
                "kids": room.kids,
                "infants": room.infants,
                "is_active": room.is_active,
                "images": [
                    {"path": image.image.url} for image in images
                ]
            }

            return JsonResponse(response)

    return JsonResponse({"error": "You should provide room id"})


def create_booking(request):
    try:
        data = json.loads(request.POST['data'])
        room = Room.objects.get(pk=data['room'])

        start = datetime.datetime.strptime(data['check_in'], "%Y-%m-%d")
        end = datetime.datetime.strptime(data['check_out'], "%Y-%m-%d")
        days = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]

        for day in days:
            Bookings.objects.create(hotel=room.hotel, date=day, room=room,
                                    client_name=request.POST['client_name'],
                                    client_email=request.POST['client_email'],
                                    phone_number=request.POST['phone_number'],
                                    time=datetime.datetime.strptime(request.POST['time'], '%H:%M'),
                                    comments=request.POST['comments'],
                                    country=request.POST['country'],
                                    address=request.POST['address'], )

        return JsonResponse({"response": 200})

    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "You should provide valid data"})
    except Exception as err:
        return JsonResponse({"error": err})


def get_bookings(request):
    room_id = request.GET['room']
    if room_id:
        if isinstance(room_id, str):
            response = []  # list of bookings
            bookings = Bookings.objects.filter(room__pk=room_id, date__gte=datetime.datetime.today())
            for booking in bookings:
                response.append({
                    "id": booking.room.id,
                    "hotel": booking.hotel.name,
                    "hotel_id": booking.hotel.id,
                    "date": booking.date,
                    "room": booking.room.name,
                    "client_name": booking.client_name,
                    "client_email": booking.client_email,
                    "phone_number": booking.phone_number,
                    "time": booking.time,
                    "comments": booking.comments,
                    "country": booking.country,
                    "address": booking.address,
                })

            return JsonResponse(response, safe=False)

    return JsonResponse({"error": "You should provide room id"})


def get_hotel_bookings(request):
    hotel_id = request.GET['hotel']
    if hotel_id:
        if isinstance(hotel_id, str):
            response = []  # list of bookings
            bookings = Bookings.objects.filter(hotel__pk=hotel_id, date__gte=datetime.datetime.today())
            for booking in bookings:
                response.append({
                    "id": booking.id,
                    "hotel_id": booking.hotel.id,
                    "hotel": booking.hotel.name,
                    "date": booking.date,
                    "room": booking.room.name,
                    "room_id": booking.room.id,
                    "client_name": booking.client_name,
                    "client_email": booking.client_email,
                    "phone_number": booking.phone_number,
                    "time": booking.time,
                    "comments": booking.comments,
                    "country": booking.country,
                    "address": booking.address,
                })

            return JsonResponse(response, safe=False)

    return JsonResponse({"error": "You should provide room id"})


def create_room(request):
    try:
        data = json.loads(request.POST['data'])
        hotel = Hotel.objects.get(id=data['id'])
        print(hotel)
        Room.objects.create()

        return JsonResponse({"response": 200})

    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "You should provide valid data"})
    except Exception as err:
        return JsonResponse({"error": err})
