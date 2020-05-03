import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from mainapp import utils


def main(request):
    data = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getHotel?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)
    images = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getImages?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)
    rooms = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getRooms?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)
    ratings = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getRatings?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)

    content = {'data': data, 'images': images, 'rooms': rooms[:4], 'host': settings.HOST, 'ratings': ratings}
    return render(request, 'mainapp/index.html', content)


def search(request):
    adults = request.GET.get('adults', 0)
    check_in = request.GET.get('check_in', '2020-05-02')
    check_out = request.GET.get('check_out', '2020-05-02')

    data = {'adults': adults, "check_in": check_in, 'check_out': check_out}
    rooms = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/filterRooms?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}&data={str(data)}').content)

    data = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getHotel?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)

    content = {'rooms': rooms, 'data': data, 'host': settings.HOST}
    return render(request, 'mainapp/search.html', content)


def room_detail(request, id):
    data = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getHotel?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)

    room = utils.decode_response(
        requests.get(f'http://{settings.HOST}/api/getRoom?room={id}&token={settings.API_TOKEN}').content)
    reviews = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getRatings?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)

    if request.method == "POST":
        if request.POST['form-type'] == 'add-rating':
            requests.post(f'http://{settings.HOST}/api/addRating/?token={settings.API_TOKEN}',
                          data={'hotel': settings.HOTEL_ID,
                                'author': request.POST['author'],
                                'text': request.POST['text'],
                                'rate': request.POST['stars']})

        elif request.POST['form-type'] == 'book-room':
            pass

        return HttpResponseRedirect(reverse('main:room', kwargs={'id': id}))

    content = {'room': room, 'data': data, 'host': settings.HOST, 'reviews': reviews[:4], 'id': id}
    return render(request, 'mainapp/room-detail.html', content)
