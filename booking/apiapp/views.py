import datetime
import json

from django.http import JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from mainapp.models import Room, Hotel, Bookings, RoomGallery, Comment
from mainapp import utils

from constructor_app.models import WebSite


def token_pass(func):
    def _decorator(request, *args, **kwargs):
        token = request.GET.get('token', '')
        site = get_object_or_404(WebSite, token=token)
        if not token or (not (site and site.is_active) and site.date_of_expiry < datetime.datetime.today()):
            return JsonResponse({"error": "Invalid API Token"}, safe=False)
        else:
            return func(request)

    return _decorator


@token_pass
def get_ratings(request):
    hotel_id = request.GET['hotel']

    if hotel_id:
        if isinstance(hotel_id, str):
            response = [{"text": comment.comment,
                         "author": comment.author,
                         "rate": comment.rate} for comment in Comment.objects.filter(hotel__id=hotel_id)]

            return JsonResponse(response, safe=False)

    return JsonResponse({"error": "You should provide hotel id"})


@token_pass
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
                        {"url": image.image.url} for image in images
                    ]
                })

            return JsonResponse(response, safe=False)

    return JsonResponse({"error": "You should provide hotel id"})


@csrf_exempt
@token_pass
def add_rating(request):
    if request.method == "POST":
        Comment.objects.create(hotel=get_object_or_404(Hotel, id=request.POST['hotel']),
                               author=request.POST['author'],
                               comment=request.POST['text'],
                               rate=request.POST['rate'])
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code': 500})


@token_pass
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


@token_pass
def get_hotel_images(request):
    hotel_id = request.GET['hotel']

    if hotel_id:
        if isinstance(hotel_id, str):
            hotel = get_object_or_404(Hotel, id=request.GET['hotel'])

            response = [{'url': image.image.url} for image in RoomGallery.objects.filter(room__hotel=hotel)]
            response.append({'url': hotel.banner.url})

            return JsonResponse(response, safe=False)

    return JsonResponse({"error": "You should provide hotel id"}, safe=False)


@token_pass
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
                    {"url": image.image.url} for image in images
                ]
            }

            return JsonResponse(response)

    return JsonResponse({"error": "You should provide room id"})

@csrf_exempt
@token_pass
def create_booking(request):
    try:
        room = Room.objects.get(pk=request.POST['room'])
        success = utils.create_room_booking(request, room.id, room.hotel.id)

        return JsonResponse({"response": 200 if success else 500})

    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "You should provide valid data"})
    except Exception as err:
        return JsonResponse({"error": err})


@token_pass
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


@token_pass
def filter_rooms(request):
    hotel_id = request.GET['hotel']
    try:
        data = json.loads(request.GET['data'].replace("\'", "\""))
        if hotel_id:
            if isinstance(hotel_id, str):
                rooms = Room.objects.filter(hotel__id=hotel_id, is_active=True, hotel__is_active=True,
                                            adult__gte=data['adults'])
                res = []

                start = datetime.datetime.strptime(data['check_in'], "%Y-%m-%d")
                end = datetime.datetime.strptime(data['check_out'], "%Y-%m-%d")
                date_list = [start + datetime.timedelta(days=x) for x in
                             range(0, (end - start).days)]  # list of dates
                hotel = get_object_or_404(Hotel, pk=hotel_id, is_active=True)

                for room in rooms:
                    flag = True
                    # if the first date element is earlier than today: return False
                    if str(date_list[0]).split(' ')[0] < str(datetime.datetime.today()).split(' ')[0]:
                        return JsonResponse([{}], safe=False)

                    # else: check for every day
                    for date in date_list:
                        # if booking for this room, at this hotel, and for this date exists: return False
                        #  select * from `table` where room = room and date = date and hotel = hotel
                        if len(Bookings.objects.filter(room=room, room__is_active=True, hotel=hotel,
                                                       date=str(date).split(' ')[0])):
                            flag = False
                            break

                    if flag:
                        res.append(room)

                response = [{
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
                        {"url": image.image.url} for image in RoomGallery.objects.filter(room=room)
                    ]
                } for room in res]

                return JsonResponse(response, safe=False)

    except json.JSONDecodeError as err:
        print(err)
        return JsonResponse({"error": "Invalid data"})

    return JsonResponse({"error": "You should provide room id"})


@token_pass
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


@token_pass
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
