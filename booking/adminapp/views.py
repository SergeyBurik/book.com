import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from mainapp.models import Bookings, Hotel


@login_required(login_url='/auth/login/')
def main(request):
    hotels = Hotel.objects.filter(user=request.user)
    bookings = []

    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]

    for hotel in hotels:
        bookings += Bookings.objects.filter(hotel=hotel)

    context = {'bookings': bookings, 'hotels': hotels, 'days': days}

    return render(request, 'adminapp/main.html', context)


@login_required(login_url='/auth/login/')
def create_hotel(request):
    return render(request, 'adminapp/create_hotel.html')
