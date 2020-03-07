from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.forms import UserRegisterForm


def join(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:
        register_form = UserRegisterForm()

    content = {'register_form': register_form}

    return render(request, 'authapp/sign_up.html', content)


def login(request):
    return render(request, 'authapp/sign_in.html', {})