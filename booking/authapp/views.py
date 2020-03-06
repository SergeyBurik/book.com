from django.shortcuts import render

# Create your views here.
def join(request):
    return render(request, 'authapp/sign_up.html', {})