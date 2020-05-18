import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from mainapp import utils
import datetime


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
    check_in = request.GET.get('check_in', datetime.datetime.today().strftime('%Y-%m-%d'))
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    check_out = request.GET.get('check_out', tomorrow.strftime('%Y-%m-%d'))

    data = {'adults': adults, "check_in": check_in, 'check_out': check_out}
    rooms = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/filterRooms?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}&data={str(data)}').content)

    data = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getHotel?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)

    content = {'rooms': rooms, 'adults': adults, 'check_in': check_in, 'check_out': check_out, 'data': data,
               'host': settings.HOST}
    return render(request, 'mainapp/search.html', content)


def room_detail(request, id):
    adults = request.GET.get('adults', 1)
    check_in = request.GET.get('check_in', None)
    check_out = request.GET.get('check_out', None)
    from_search = request.GET.get('search', False)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    data = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getHotel?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)

    room = utils.decode_response(
        requests.get(f'http://{settings.HOST}/api/getRoom?room={id}&token={settings.API_TOKEN}').content)
    reviews = utils.decode_response(
        requests.get(
            f'http://{settings.HOST}/api/getRatings?hotel={settings.HOTEL_ID}&token={settings.API_TOKEN}').content)

    if from_search:
        available = True  # if user came here from search, then the room is free
    else:
        available = False  # user need to check if the room is free

    if request.method == "POST":
        if request.POST['form-type'] == 'add-rating':
            requests.post(f'http://{settings.HOST}/api/addRating/?token={settings.API_TOKEN}',
                          data={'hotel': settings.HOTEL_ID,
                                'author': request.POST['author'],
                                'text': request.POST['text'],
                                'rate': request.POST['stars']})

        elif request.POST['form-type'] == 'book-room':
            requests.post(f'http://{settings.HOST}/api/createBooking/?token={settings.API_TOKEN}',
                          data={"room": room['id'],
                                'check_in': request.POST.get('check_in', None),
                                'check_out': request.POST.get('check_out', None),
                                'client_name': request.POST.get('first_name'),
                                'client_surname': request.POST.get('last_name'),
                                'email': request.POST.get('email'),
                                'phone': request.POST.get('phone_number'),
                                'time': request.POST.get('time'),
                                'comments': request.POST.get('comments'),
                                'country': request.POST.get('country'),
                                'address': request.POST.get('address'),
                                })

        return HttpResponseRedirect(reverse('main:room', kwargs={'id': id}))

    content = {'room': room, 'data': data, 'host': settings.HOST, 'adults': adults, 'check_in': check_in,
               'check_out': check_out, 'today': today, 'tomorrow': tomorrow,
               'reviews': reviews[:3], 'id': id, 'available': available,
               'from_search': from_search}
    return render(request, 'mainapp/room-detail.html', content)


def ajax_check_availability(request):
    room = request.GET.get('room')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    start = datetime.datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.datetime.strptime(check_out, "%Y-%m-%d")
    date_list = [start + datetime.timedelta(days=x) for x in
                 range(0, (end - start).days)]  # list of dates

    bookings = utils.decode_response(
        requests.get(f'http://{settings.HOST}/api/getRoomBookings?room={room}&token={settings.API_TOKEN}').content)

    for booking in bookings:
        if datetime.datetime.strptime(booking['date'], "%Y-%m-%d") in date_list:
            return JsonResponse({'code': 404, 'message': 'Not available'}, safe=False)

    return JsonResponse({'code': 200, 'message': 'Available'}, safe=False)
