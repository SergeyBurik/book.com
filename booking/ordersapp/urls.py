from django.urls import path
from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.main, name='main'),
    path('success', ordersapp.success, name='success'),
    # path('pay/<int:hotel_id>/<int:room_id>/', ordersapp.success, name='success'),
    # path('pay/', ordersapp.pay_with_robokassa, name='pay'),
    # path('pay/<int:hotel_id>/room/<int:room_id>/', ordersapp.pay_with_robokassa, name='pay'),
    # path('', ordersapp.OrderList.as_view(), name='index'),
    # path('bookings/<int:hotel_id>/room/<int:room_id>/', ordersapp.book_room, name='book_room'),
    # path('bookings/<int:hotel_id>/', ordersapp.bookings_main, name='bookings_main'),
    # path('order/forming/complete/<pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),
    # path('order/create/', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    # path('order/read/<pk>/', ordersapp.OrderRead.as_view(), name='order_read'),
    # path('order/update/<pk>/', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    # path('order/delete/<pk>)/', ordersapp.OrderDelete.as_view(), name='order_delete'),
    # path('product/<pk>/price/', ordersapp.get_product_price),
]
