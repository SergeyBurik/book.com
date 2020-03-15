import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from mainapp.models import Bookings, Hotel, Room


@login_required(login_url='/auth/login/')
def main(request):
    hotels = Hotel.objects.filter(user=request.user)
    bookings = []
    rooms = []

    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]

    for hotel in hotels:
        bookings += Bookings.objects.filter(hotel=hotel)
        rooms += Room.objects.filter(hotel=hotel)

    context = {'bookings': bookings, 'hotels': hotels, 'days': days, 'rooms': rooms}

    return render(request, 'adminapp/main.html', context)


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
