from django.urls import path
from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.main, name='main'),
    path('success', ordersapp.success, name='success'),
    # path('pay/<int:hotel_id>/<int:room_id>/', ordersapp.success, name='success'),
    # path('pay/', ordersapp.pay_with_robokassa, name='pay'),
    path('pay/<int:hotel_id>/room/<int:room_id>/<str:check_in>/<str:check_out>/', ordersapp.checkout, name='pay'),
]
