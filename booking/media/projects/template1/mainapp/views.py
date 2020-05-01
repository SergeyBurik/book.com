import requests
from django.shortcuts import render
from django.conf import settings
from mainapp import utils


def main(request):
    data = utils.decode_response(
        requests.get(f'http://{settings.HOST}/api/getHotel?hotel={settings.HOTEL_ID}').content)
    images = utils.decode_response(
        requests.get(f'http://{settings.HOST}/api/getImages?hotel={settings.HOTEL_ID}').content)
    rooms = utils.decode_response(
        requests.get(f'http://{settings.HOST}/api/getRooms?hotel={settings.HOTEL_ID}').content)
    ratings = utils.decode_response(
        requests.get(f'http://{settings.HOST}/api/getRatings?hotel={settings.HOTEL_ID}').content)


    content = {'data': data, 'images': images, 'rooms': rooms[:4], 'host': settings.HOST, 'ratings':ratings}
    return render(request, 'mainapp/index.html', content)
