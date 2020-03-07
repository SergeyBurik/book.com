from django.urls import path
from authapp import views as authapp

app_name = 'authapp'


urlpatterns = [
    path('join/', authapp.join, name='join'),  # sign up page url
    path('login/', authapp.login, name='login'),  # sign in page url


]
