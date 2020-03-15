from django.urls import path
from adminapp import views as adminapp

app_name = 'authapp'

urlpatterns = [
    path('main/', adminapp.main, name='main'),
    path('create_hotel/', adminapp.create_hotel, name='create_hotel'),
    path('create_room/', adminapp.create_room, name='create_room'),
]
