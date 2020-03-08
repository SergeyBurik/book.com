import os

from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from authapp.forms import UserRegisterForm
from authapp.models import UserActivation, User

from django.conf import settings


def join(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('Account Verification letter has been sent!')
            else:
                print('Failed to send account verification letter')

            return HttpResponseRedirect(reverse('main'))
    else:
        register_form = UserRegisterForm()

    content = {'register_form': register_form}

    return render(request, 'authapp/sign_up.html', content)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        print(user)
        print(email)
        print(password)

        if user:
            auth.login(request, user)
            print(user)
            return HttpResponseRedirect(reverse('main'))

    return render(request, 'authapp/sign_in.html', {})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def send_verify_mail(user):
    activation_key = UserActivation.objects.get(user=user).activation_key
    verify_link = reverse('auth:verify', args=[user.email, activation_key])
    title = f'Account Verification {user.name} {user.surname}'

    print(os.path.join(settings.BASE_DIR, 'static', 'assets', 'letter.html'))

    html_m = render_to_string('authapp/letter.html',
                              {'username': user.name, 'link': settings.DOMAIN_NAME + verify_link})

    return send_mail(title, '', settings.EMAIL_HOST_USER, [user.email], html_message=html_m,
                     fail_silently=False)


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

        return HttpResponseRedirect(reverse('main'))

    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main'))
