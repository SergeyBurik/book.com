from django.urls import path
from mainapp import views as mainapp

app_name = 'constructor_app'

urlpatterns = [
    path('', mainapp.main, name='main'),

]
