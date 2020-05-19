from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('search/', mainapp.search, name='search'),
    path('room/<int:id>/', mainapp.room_detail, name='room'),
    path('ajax/check_availability/', mainapp.ajax_check_availability, name='ajax_check_availability'),
]
