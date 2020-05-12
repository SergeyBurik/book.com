import datetime
import os
from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.utils.deconstruct import deconstructible

from authapp.models import User
from authapp.variables import country_dict
from mainapp.variables import arrival_time


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)

        return os.path.join(self.path, filename)


path_and_rename = PathAndRename("rooms/")


class Hotel(models.Model):
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
        ordering = ['name']

    ONE = 'ON'
    TWO = 'TW'
    THREE = 'TR'
    FOUR = 'FR'
    FIVE = 'FV'
    STARS_CHOICES = [
        (ONE, '1*'),
        (TWO, '2*'),
        (THREE, '3*'),
        (FOUR, '4*'),
        (FIVE, '5*'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    name = models.CharField(verbose_name='Название отеля', max_length=64,
                            unique=True)
    phone_number = models.CharField(verbose_name='Номер телефона', default='',
                                    max_length=20)
    location = models.CharField(verbose_name='Адрес отеля', default='',
                                max_length=200)
    description = models.TextField(verbose_name='Описание отеля', blank=True)
    stars = models.CharField(max_length=2, choices=STARS_CHOICES, default=ONE)
    banner = models.ImageField(default='', upload_to='hotels/banners/')
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    def __str__(self):
        return self.name

    def get_count_facility(self):
        items = self.hotelfacility.select_related()
        return len(items)

    def get_facility(self):
        arr = []
        items = self.hotelfacility.select_related()
        for i in range(len(items)):
            arr.append(items[i].get_name())
        return arr

    def get_facility_icon(self):
        arr = []
        items = self.hotelfacility.select_related()
        for i in range(len(items)):
            arr.append(items[i].get_icon())
        return arr


class Facility(models.Model):
    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'

    # icon = models.ImageField(default='', upload_to='hotels/icons/')
    icon = models.ImageField(upload_to=path_and_rename,
                             verbose_name='Facility icon')
    name = models.CharField(verbose_name='Facility', max_length=64,
                            unique=True)

    @staticmethod
    def get_items():
        return Facility.objects.all().order_by('name')

    def __str__(self):
        return self.name


class HotelFacility(models.Model):
    class Meta:
        verbose_name = ' Hotel Facility'
        verbose_name_plural = 'Hotel Facilities'

    hotel = models.ForeignKey(Hotel, related_name="facility",
                              on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, verbose_name='Facility name',
                                 on_delete=models.CASCADE)

    def get_icon(self):
        return self.facility.icon

    def get_name(self):
        return self.facility.name

    @staticmethod
    def get_items():
        return HotelFacility.objects.all().order_by('facility')

    def __str__(self):
        return self.facility.name


class RoomAgent(models.Model):
    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'
        ordering = ['name']

    name = models.CharField(verbose_name='Имя агента', max_length=64,
                            unique=True)
    description = models.CharField(verbose_name='Краткое описание агента',
                                   max_length=128, blank=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    def __str__(self):
        return self.name


class RoomManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
            )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class Room(models.Model):
    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ['name']

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default='')
    name = models.CharField(verbose_name='Имя', max_length=32)
    price = models.DecimalField(verbose_name='Цена', max_digits=12,
                                decimal_places=2, default=0)
    description = models.TextField(verbose_name='Описание', blank=True)
    adult = models.PositiveIntegerField(verbose_name='Взрослый', default=0)
    kids = models.PositiveIntegerField(verbose_name='Детский', default=0)
    infants = models.PositiveIntegerField(verbose_name='Детский', default=0)
    # image = models.ImageField(upload_to=path_and_rename, blank=True)
    is_active = models.BooleanField(verbose_name='Номер активен', default=True)

    objects = RoomManager()

    def __str__(self):
        return "{} ({})".format(self.name, self.hotel.name)

    def __unicode__(self):
        return self.name


class RoomGallery(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['image']

    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             verbose_name='Название номера')
    image = models.ImageField(upload_to=path_and_rename,
                              verbose_name='Изображение номера')
    is_avatar = models.BooleanField(verbose_name='Главное изображение номера', default=False)

    def __str__(self):
        return self.room.name


# def make_avatar(args*):


class Bookings(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default='')
    date = models.DateField()  # date of booking
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # room which we are trying to book
    client_name = models.CharField(max_length=100)
    client_email = models.CharField(max_length=100)  # client's email
    phone_number = models.CharField(max_length=20,  verbose_name="Client's phone number")
    time = models.CharField(max_length=50, choices=arrival_time,
                            default='12:00')  # approximate time of check in
    comments = models.CharField(max_length=500)  # client's requests
    country = models.CharField(max_length=50, choices=country_dict,
                               default='Russia')
    address = models.CharField(max_length=100)  # client's address of living

    def __str__(self):
        return 'Room Booking {} - {}'.format(self.room.name, self.room.hotel.name)


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['author']

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    author = models.CharField(verbose_name='Author', max_length=32)
    comment = models.CharField(verbose_name='comment', max_length=200)
    rate = models.PositiveIntegerField()
    pub_date = models.DateField(verbose_name='создан', default=datetime.date.today)

    def __str__(self):
        return self.author
