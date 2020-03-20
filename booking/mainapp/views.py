from django.shortcuts import render


def main_page(request):
    user = request.user

    return render(request, 'mainapp/index.html', {'user': user})
