from django.core.management.base import BaseCommand
from mainapp.models import Facility, HotelFacility
# from authapp.models import User

import json
import os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        facilities = load_from_json('facility')
        Facility.objects.all().delete()

        for facility in facilities:
            new_facility = Facility(**facility)
            new_facility.save()

        hotel_facilities = load_from_json('hotelfacility')
        HotelFacility.objects.all().delete()
        for facility in hotel_facilities:
            new_f = HotelFacility(**facility)
            new_f.save()

        # hotels = load_from_json('hotels')
        # Hotel.objects.all().delete()
        # for hotel in hotels:
        #     new_hotel = Hotel(**hotel)
        #     new_hotel.save()
        #
        # rooms = load_from_json('rooms')
        #
        # Room.objects.all().delete()
        # for room in rooms:
        #     hotel_name = room["hotel"]
        #     # Получаем категорию по имени
        #     _hotel = Hotel.objects.get(name=hotel_name)
        #     # Заменяем название категории объектом
        #     room['hotel'] = _hotel
        #     new_room = Room(**room)
        #     new_room.save()

        # Создаем суперпользователя при помощи менеджера модели
        # super_user = User.objects.create_superuser('admin', 'admin@admin.rul', 'admin')
