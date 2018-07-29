from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse


@login_required
def index(request):
    return HttpResponseRedirect(reverse('decks'))


def login(request):
    return render(request, 'login.html')


def authenticate_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user:
        login_user(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('login'))


def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse('index'))


def register(request, password_mismatch=False):
    if password_mismatch:
        return render(request, 'register.html', {'password_mismatch' : True})
    else:
        return render(request, 'register.html', {'password_mismatch' : False})


def create_user(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password-confirm')

    if password != password_confirm:
        return HttpResponseRedirect(reverse('register', args=(True,)))

    User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

    return HttpResponseRedirect(reverse('register-success'))


def register_success(request):
    return render(request, 'register_successful.html')


@login_required
def decks(request):
    return render(request, 'index.html')
