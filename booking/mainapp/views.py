from django.shortcuts import render
from authapp.models import User


def main_page(request):
    user = request.user

    print(user.is_authenticated)
    return render(request, 'mainapp/index.html', {'user': user})
