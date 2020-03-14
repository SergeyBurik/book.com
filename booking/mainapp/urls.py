from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main_page, name='main'),  # sign up page url

]
