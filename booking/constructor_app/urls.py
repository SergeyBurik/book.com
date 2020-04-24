from django.urls import path
from constructor_app import views as constructor

app_name = 'constructor_app'

urlpatterns = [
    path('', constructor.main, name='main'),
    path('detail/template-<int:id>/', constructor.about_template, name='about_template'),
    path('pack/<int:id>/', constructor.pack_project, name='pack'),
]
