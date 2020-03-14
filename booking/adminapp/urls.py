from django.urls import path
from adminapp import views as adminapp

app_name = 'authapp'

urlpatterns = [
    path('main/', adminapp.main, name='main')
]
