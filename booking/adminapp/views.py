from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

@login_required(login_url='/auth/login/')
def main(request):
    return render(request, 'adminapp/main.html', {})
