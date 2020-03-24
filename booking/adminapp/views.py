import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from mainapp.models import Bookings, Hotel, Room

from adminapp.forms import HotelForm, RoomForm


@login_required(login_url='/auth/login/')
def main(request):
    hotels = Hotel.objects.filter(user=request.user, is_active=True)
    bookings = []
    rooms = []

    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]

    for hotel in hotels:
        bookings += Bookings.objects.filter(hotel=hotel)
        rooms += Room.objects.filter(hotel=hotel)

    context = {'bookings': bookings, 'hotels': hotels, 'days': days, 'rooms': rooms}

    return render(request, 'adminapp/main.html', context)


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
        image = request.FILES['image']

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

        print(name)
        print(hotel)

        # create room
        Room.objects.create(hotel=hotel, name=name,
                            price=int(price), description=description,
                            adult=int(adults), kids=int(kids),
                            infants=int(infants), image=image,
                            is_active=True)

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
        if form.is_valid():
            obj = form.save(commit=False)

            obj.save()

            messages.success(request, "You successfully updated the post")

            context = {'form': form}

            return HttpResponseRedirect(reverse('management:rooms'))

        else:
            messages.warning(request, "The form was not updated successfully.")

    context = {'form': form, 'hotel_id': hotel_id, 'room_id': room_id}
    return render(request, 'adminapp/edit_room.html', context)


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

        print(hotel_name)
        print(description)
        print(stars)
        print(banner)
        print(request.user)

        Hotel.objects.create(user=request.user,
                             name=hotel_name,
                             description=description,
                             stars=stars,
                             banner=banner,
                             is_active=True)

        return HttpResponseRedirect(reverse('management:main'))

    return render(request, 'adminapp/create_hotel.html')
