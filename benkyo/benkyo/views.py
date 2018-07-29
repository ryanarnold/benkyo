from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Deck, DeckUser


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


def register(request, password_mismatch='no'):
    if password_mismatch == 'yes':
        return render(request, 'register.html', {'password_mismatch' : 'yes'})
    else:
        return render(request, 'register.html', {'password_mismatch' : 'no'})


def create_user(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password-confirm')

    if password != password_confirm:
        return HttpResponseRedirect(reverse('register', args=('yes',)))

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
    decks_of_user = DeckUser.objects.filter(user=request.user)
    decks = [deck.deck for deck in decks_of_user]

    context = {
        'decks': decks
    }

    return render(request, 'decks.html', context)


@login_required
def decks_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        private = True if request.POST.get('private') == 'yes' else False

        deck = Deck.objects.create(
            name=name,
            private=private
        )

        DeckUser.objects.create(
            deck=deck,
            user=request.user,
            role_cd='O'
        )

        return HttpResponseRedirect(reverse('decks-create-successful'))

    return render(request, 'decks_create.html')


@login_required
def decks_create_successful(request):
    return render(request, 'decks_create_successful.html')


@login_required
def decks_delete_confirm(request, deck_id):
    context = {
        'deck': Deck.objects.get(deck_id=deck_id)
    }

    return render(request, 'decks_delete_confirm.html', context)


@login_required
def decks_delete(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)
    DeckUser.objects.get(deck=deck).delete()
    deck.delete()    

    return HttpResponseRedirect(reverse('decks-delete-successful'))


@login_required
def decks_delete_successful(request):
    return render(request, 'decks_delete_successful.html')


@login_required
def decks_edit(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        private = True if request.POST.get('private') == 'yes' else False

        deck.name = name
        deck.private = private
        deck.save()

    context = {
        'deck': deck
    }

    return render(request, 'decks_edit.html', context)
