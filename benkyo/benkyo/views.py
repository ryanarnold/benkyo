from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate
from django.urls import reverse


@login_required
def index(request):
    return render(request, 'index.html')


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


def register(request):
    return render(request, 'register.html')
