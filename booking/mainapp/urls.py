from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main_page, name='main'),  # sign up page url
    path('bookings/<int:hotel_id>/', mainapp.bookings_main, name='bookings_main'),

]
