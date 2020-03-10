from django.shortcuts import render


def main_page(request):
    user = request.user

    print(user.is_authenticated)
    return render(request, 'mainapp/index.html', {'user': user})
