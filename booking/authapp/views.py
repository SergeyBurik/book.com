import os

from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from authapp.forms import UserRegisterForm, UserLoginForm
from authapp.models import UserActivation, User

from django.conf import settings

from authapp.variables import country_dict


def join(request):
    title = 'Register'
    countries = country_dict
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('Account Verification letter has been sent!')
            else:
                print('Failed to send account verification letter')

            return HttpResponseRedirect(reverse('main:main'))
    else:
        register_form = UserRegisterForm()

    content = {'register_form': register_form,
               'countries': countries,
               'title': title,
               }

    return render(request, 'authapp/sign_up.html', content)


def login(request):
    login_form = UserLoginForm(data=request.POST)

    print(login_form.is_valid())
    print(login_form.errors)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)

        user = auth.authenticate(username=username, password=password)

        if user and user.active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:main'))
    else:
        login_form = UserLoginForm()

    content = {'login_form': login_form}
    return render(request, 'authapp/sign_in.html', content)


def send_verify_mail(user):
    activation_key = UserActivation.objects.get(user=user).activation_key
    verify_link = reverse('auth:verify', args=[user.email, activation_key])
    title = 'Account Verification {} {}'.format(user.name, user.surname)

    print(os.path.join(settings.BASE_DIR, 'static', 'assets', 'letter.html'))

    html_m = render_to_string('authapp/letter.html',
                              {'username': user.name,
                               'link': settings.DOMAIN_NAME + verify_link}
                              )

    return send_mail(title, '', settings.EMAIL_HOST_USER,
                     [user.email], html_message=html_m, fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        user_activation = UserActivation.objects.get(user=user)

        if user_activation.activation_key == activation_key and not user_activation.is_activation_key_expired():
            print('activating...')
            user.active = True
            user.save()
            auth.login(request, user)
            print(f'successfully activated user: {user}')
        else:
            print(f'error activation user: {user}')

        return HttpResponseRedirect(reverse('main:main'))

    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:main'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main'))
