from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Card, CardTag, Deck, DeckUser


@login_required
def index(request):
    return HttpResponseRedirect(reverse('decks'))


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_user(request, user)
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'login.html')


def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    email = ''
    username = ''
    password_mismatch = False

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')

        if password == password_confirm:
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            return HttpResponseRedirect(reverse('register-success'))
        else:
            password_mismatch = True
    
    context = {
        'email': email,
        'username': username,
        'password_mismatch': password_mismatch
    }

    return render(request, 'register.html', context)


def register_success(request):
    return render(request, 'register_successful.html')


@login_required
def decks(request):
    decks_of_user = DeckUser.objects.filter(user=request.user)
    decks = [deck.deck for deck in decks_of_user]

    for deck in decks:
        deck.card_count = Card.objects.filter(deck=deck).count()

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

        return HttpResponseRedirect(reverse('decks'))

    return render(request, 'decks_create.html')


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
    cards = Card.objects.filter(deck=deck)

    if request.method == 'POST':
        name = request.POST.get('name')
        private = True if request.POST.get('private') == 'yes' else False

        deck.name = name
        deck.private = private
        deck.save()

    context = {
        'deck': deck,
        'cards': cards,
        'first_card': cards[0] if len(cards) > 0 is not None else None
    }

    return render(request, 'decks_edit.html', context)


@login_required
def cards_add(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)

    if request.method == 'POST':
        front = request.POST.get('front')
        back = request.POST.get('back')

        card = Card.objects.create(
            deck=deck,
            front=front,
            back=back
        )

        tags = [tag.strip() for tag in request.POST.get('tags').split(',')]
        
        for tag in tags:
            CardTag.objects.create(
                card=card,
                tag=tag
            )

        return HttpResponseRedirect(reverse('decks-edit', args=(deck_id,)))
    
    context = {
        'deck': deck
    }

    return render(request, 'cards_add.html', context)


@login_required
def cards_edit(request, deck_id, card_id):
    deck = Deck.objects.get(deck_id=deck_id)
    card = Card.objects.get(card_id=card_id)
    tags = CardTag.objects.filter(card=card)

    if request.method == 'POST':
        front = request.POST.get('front')
        back = request.POST.get('back')

        card.front = front
        card.back = back

        card.save()

        # Reset all tags for the card
        CardTag.objects.filter(card=card).delete()

        tags = [tag.strip() for tag in request.POST.get('tags').split(',')]
        for tag in tags:
            CardTag.objects.create(
                card=   card,
                tag=tag
            )

        return HttpResponseRedirect(reverse('decks-edit', args=(deck_id,)))

    context = {
        'deck': deck,
        'card': card,
        'tags_string': ','.join([tag.tag for tag in tags])
    }

    return render(request, 'cards_edit.html', context)


@login_required
def cards_delete(request, deck_id, card_id):
    deck = Deck.objects.get(deck_id=deck_id)
    card = Card.objects.get(card_id=card_id)

    if request.method == 'POST':
        card.delete()

        return HttpResponseRedirect(reverse('decks-edit', args=(deck_id,)))

    context = {
        'deck': deck,
        'card': card
    }

    return render(request, 'cards_delete_confirm.html', context)


@login_required
def cards_delete_all(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)

    if request.method == 'POST':
        cards = Card.objects.filter(deck=deck)
        cards.delete()

        return HttpResponseRedirect(reverse('decks-edit', args=(deck_id,)))

    context = {
        'deck': deck
    }
    
    return render(request, 'cards_delete_all.html', context)

@login_required
def cards_import(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)

    if request.method == 'POST':
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage()
        filename = fs.save(upload_file.name, upload_file)
        uploaded_file_url = fs.url(filename)

        deck.import_cards_from_file(filename)
        
        return HttpResponseRedirect(reverse('decks-edit', args=(deck_id,)))

    context = {
        'deck': deck,
    }

    return render(request, 'cards_import.html', context)
