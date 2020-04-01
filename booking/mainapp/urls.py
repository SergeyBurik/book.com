from django.urls import path
from mainapp import views as mainapp
from ordersapp import views as ordersapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main_page, name='main'),  # sign up page url
    path('bookings/<int:hotel_id>/', mainapp.bookings_main, name='bookings_main'),
    path('<int:hotel_id>/room/<int:room_id>/', mainapp.book_room, name='book_room'),
    path('bookings/<int:hotel_id>/room/<int:room_id>/pay/', ordersapp.pay_with_robokassa, name='pay'),
    path('pay/', mainapp.pay_with_robokassa, name='pay_with_robokassa'),
]
