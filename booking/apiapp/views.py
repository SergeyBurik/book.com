import datetime
import json

from django.http import JsonResponse
# from django.shortcuts import render

# Create your views here.
from mainapp.models import Room, Hotel, Bookings, RoomGallery


def get_rooms(request):
    hotel_id = request.GET['hotel']
    if hotel_id:
        if isinstance(hotel_id, int):
            response = []  # list of rooms
            rooms = Room.objects.filter(hotel__pk=hotel_id, is_active=True)
            for room in rooms:
                response.append({
                    "hotel": room.hotel,
                    "name": room.name,
                    "price": room.price,
                    "description": room.description,
                    "adult": room.adult,
                    "kids": room.kids,
                    "infants": room.infants,
                    "is_active": room.is_active,
                })

            return JsonResponse(response)

    return JsonResponse({"error": "You should provide hotel id"})


def get_hotel(request):
    hotel_id = request.GET['hotel']
    if hotel_id:
        if isinstance(hotel_id, int):
            hotel = Hotel.objects.filter(hotel__pk=hotel_id, is_active=True)[0]
            response = {
                "user": hotel.user,
                "name": hotel.name,
                "phone_number": hotel.phone_number,
                "location": hotel.location,
                "description": hotel.description,
                "stars": hotel.stars,
                "banner": hotel.banner.url,
            }

            return JsonResponse(response)

    return JsonResponse({"error": "You should provide hotel id"})


def get_room(request):
    room_id = request.GET['room']
    if room_id:
        if isinstance(room_id, int):
            room = Room.objects.filter(pk=room_id, is_active=True)[0]
            images = RoomGallery.objects.filter(room=room)

            response = {
                "hotel": room.hotel,
                "name": room.name,
                "price": room.price,
                "description": room.description,
                "adult": room.adult,
                "kids": room.kids,
                "infants": room.infants,
                "is_active": room.is_active,
                "images": [
                    {"path": image.url} for image in images
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
                                    address=request.POST['address'],)

        return JsonResponse({"response": 200})

    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "You should provide valid data"})
    except Exception as err:
        return JsonResponse({"error": err})
