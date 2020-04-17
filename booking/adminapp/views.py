import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from mainapp.models import Bookings, Hotel, Room, RoomGallery
from geopy.geocoders import Nominatim
from adminapp.forms import HotelForm, RoomForm
from adminapp import utils
from mainapp.utils import check_booking, insert_booking, send_confirmation_mail


@login_required(login_url='/auth/login/')
def main(request):
    hotels = Hotel.objects.filter(user=request.user, is_active=True)
    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]
    now = datetime.datetime.now()

    hotel_data = []
    for hotel in hotels:
        hotel_data.append({"name": hotel.name,
                           "rooms": [{"id": room.id,
                                      "name": room.name,
                                      "price": room.price} for room in
                                     Room.objects.filter(hotel=hotel, is_active=True)]})

    bookings = [booking for hotel in Hotel.objects.filter(user=request.user, is_active=True) for booking in
                Bookings.objects.filter(hotel=hotel)]

    print(hotel_data)

    context = {'bookings': bookings, 'hotels': hotels, 'days': days, 'rooms': rooms,
               'now': f'{now.hour}:{now.minute}', 'hotel_data': hotel_data}

    if request.method == "POST":
        check_in = request.POST.get('start', None)
        check_out = request.POST.get('end', None)
        room_id = request.POST.get('room', None)
        hotel_id = request.POST.get('hotel', None)
        client_name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        time = request.POST.get('time', None)
        comments = request.POST.get('comments', None)
        country = request.POST.get('country', None)
        address = request.POST.get('address', None)

        room = get_object_or_404(Room, id=room_id)
        hotel = get_object_or_404(Hotel, id=hotel_id)

        if room.hotel.id == hotel.id:
            if check_booking(check_in, check_out, room_id, hotel_id):  # if there are not any reservations
                insert_booking(hotel, check_in, check_out, room,
                               f'{client_name}', email, phone, time,
                               comments, country, address)
                send_confirmation_mail(hotel_id, room_id, check_in, check_out, f'{client_name}')

                return HttpResponseRedirect(reverse('management:main'))
            else:
                messages.error(request, 'Unable to create booking')
        else:
            messages.error(request, 'Unable to create booking')

    return render(request, 'adminapp/main.html', context)


# function that checks the hotel's address
def ajax_check_address(request):
    # if address is valid and function returned coordinates -> address passed check
    # else coordinates list is empty
    address = request.GET.get('address', None)

    geolocator = Nominatim(user_agent="check_address")
    location = geolocator.geocode(address)
    if location:
        coordinates = [location.latitude, location.longitude]
        message = ''
    else:
        coordinates = []
        message = 'Invalid address'

    print(location)
    print(address)
    print()

    return JsonResponse({'coordinates': coordinates, 'address': location.address,
                         'message': message})


# function that creates room in hotel
@login_required(login_url='/auth/login/')
def create_room(request):
    hotels = Hotel.objects.filter(user=request.user, is_active=True)

    if request.method == 'POST':
        # get data
        hotel = request.POST['hotel']
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        adults = request.POST['adults']
        kids = request.POST['kids']
        infants = request.POST['infants']
        images = request.POST.get('image_count', 0)
        print(images)

        # try:
        # get hotel
        hotel = Hotel.objects.get(name=hotel)
        # try to find a room with the same name
        rooms = Room.objects.filter(hotel=hotel, name=name)

        if rooms:
            try:
                # get the last room's name
                # and get the count number ex. 'Room 1' (result - '1')
                existing_room_count_number = int(rooms.reverse()[0].name.split(' ')[-1])
                # increase it
                existing_room_count_number += 1
                # change room name to not duplicate room's name
                name = f'{name} {existing_room_count_number}'
            except ValueError:
                name = f'{name} 1'

        # create room
        Room.objects.create(hotel=hotel, name=name,
                            price=int(price), description=description,
                            adult=int(adults), kids=int(kids),
                            infants=int(infants),
                            is_active=True)

        room = Room.objects.get(hotel=hotel, name=name,
                                price=int(price), description=description,
                                adult=int(adults), kids=int(kids),
                                infants=int(infants),
                                is_active=True)
        count = 1
        for image in range(1, int(images) + 1):
            image_file = request.FILES.get(f'image-{image}')
            if image_file:
                if count == 1:
                    RoomGallery.objects.create(room=room, image=image_file, is_avatar=True)
                    count += 1
                else:
                    RoomGallery.objects.create(room=room, image=image_file)

        return HttpResponseRedirect(reverse('management:main'))

        # except Exception as err:
        # print(err)

    context = {'hotels': hotels}
    return render(request, 'adminapp/create_room.html', context)


# page of editing hotel details
@login_required(login_url='/auth/login/')
def edit_room(request, hotel_id, room_id):
    # if there is such room
    hotel = get_object_or_404(Hotel, pk=hotel_id, user=request.user)
    room = get_object_or_404(Room, pk=room_id, hotel=hotel, is_active=True)

    form = RoomForm(request.POST or None, request.FILES or None, instance=room)

    if request.method == 'POST':
        # saving images
        images = request.POST.get('image_count', 0)
        for image in range(1, int(images) + 1):
            image_file = request.FILES.get(f'image-{image}')
            if image_file:
                RoomGallery.objects.create(room=room, image=image_file)
        if form.is_valid():
            obj = form.save(commit=False)

            obj.save()

            messages.success(request, "You successfully updated the room")

            context = {'form': form}

            return HttpResponseRedirect(reverse('management:rooms'))

        else:
            messages.warning(request, "The form was not updated successfully.")

    images = RoomGallery.objects.filter(room=room, room__hotel=hotel)
    context = {'form': form, 'hotel_id': hotel_id, 'room_id': room_id, 'room': room, 'images': images}
    return render(request, 'adminapp/edit_room.html', context)


def ajax_delete_image(request):
    try:
        room = request.GET.get('room', None)
        hotel = request.GET.get('hotel', None)
        image = request.GET.get('image', None)
        RoomGallery.objects.get(room__pk=room, room__hotel__pk=hotel,
                                image__contains=image.replace('/media/', '')).delete()
        return JsonResponse({'code': 200})
    except Exception as err:
        print(err)
        return JsonResponse({'code': 500})


# page of editing room details
@login_required(login_url='/auth/login/')
def edit_hotel(request, pk):
    # if there is such hotel
    hotel = get_object_or_404(Hotel, pk=pk, user=request.user, is_active=True)

    form = HotelForm(request.POST or None, request.FILES or None, instance=hotel)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)

            obj.save()

            messages.success(request, "You successfully updated the post")

            context = {'form': form}

            return HttpResponseRedirect(reverse('management:hotels'))

        else:
            messages.warning(request, "The form was not updated successfully.")

    context = {'form': form, 'pk': pk}

    return render(request, 'adminapp/edit_hotel.html', context)


# page of hotel details
@login_required(login_url='/auth/login/')
def hotels(request):
    hotels_ = Hotel.objects.filter(user=request.user, is_active=True)

    content = {'hotels': hotels_}
    return render(request, 'adminapp/hotels.html', content)


# page of room details
@login_required(login_url='/auth/login/')
def rooms(request):
    hotels = Hotel.objects.filter(user=request.user, is_active=True)
    rooms_ = []

    for hotel in hotels:
        rooms_ += Room.objects.filter(hotel=hotel)

    content = {'rooms': rooms_}
    return render(request, 'adminapp/rooms.html', content)


# function which creates hotel
@login_required(login_url='/auth/login/')
def create_hotel(request):
    if request.method == 'POST':
        hotel_name = request.POST['name']
        description = request.POST['description']
        stars = request.POST['stars']
        banner = request.FILES['banner']
        location = request.POST['location']
        phone = request.POST['number']

        location = utils.get_address(location)

        Hotel.objects.create(user=request.user,
                             name=hotel_name,
                             description=description,
                             stars=stars,
                             banner=banner,
                             location=location,
                             phone_number=phone,
                             is_active=True)

        return HttpResponseRedirect(reverse('management:main'))

    return render(request, 'adminapp/create_hotel.html')
