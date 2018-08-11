from random import shuffle
import json
import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Card, CardTag, Deck, DeckUser, Review, Settings
from .util import split_comma_separated_into_list

HTTP_POST = 'POST'

INDEX_URL = 'index'
REGISTER_SUCCESS_URL = 'register-success'
DECKS_URL = 'decks'
DECKS_EDIT_URL = 'decks-edit'
REVIEW_END_URL = 'review-end'

CARDS_ADD_HTML = 'cards_add.html'
CARDS_DELETE_ALL_HTML = 'cards_delete_all.html'
CARDS_DELETE_CONFIRM_HTML = 'cards_delete_confirm.html'
CARDS_EDIT_HTML = 'cards_edit.html'
CARDS_IMPORT_HTML = 'cards_import.html'
DECKS_HTML = 'decks.html'
DECKS_CREATE_HTML = 'decks_create.html'
DECKS_DELETE_CONFIRM_HTML = 'decks_delete_confirm.html'
DECKS_EDIT_HTML = 'decks_edit.html'
LOGIN_HTML = 'login.html'
REGISTER_HTML = 'register.html'
REGISTER_SUCCESSFUL_HTML = 'register_successful.html'
REVIEW_START_HTML = 'review_start.html'
REVIEW_HTML = 'review.html'
REVIEW_END_HTML = 'review_end.html'

@login_required
def index(request):
    return HttpResponseRedirect(reverse(DECKS_URL))


def login(request):
    if request.method == HTTP_POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_user(request, user)
            return HttpResponseRedirect(reverse(INDEX_URL))

    return render(request, LOGIN_HTML)


def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse(INDEX_URL))


def register(request):
    email = ''
    username = ''
    password_mismatch = False

    if request.method == HTTP_POST:
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
            return HttpResponseRedirect(reverse(REGISTER_SUCCESS_URL))
        else:
            password_mismatch = True
    
    context = {
        'email': email,
        'username': username,
        'password_mismatch': password_mismatch
    }

    return render(request, REGISTER_HTML, context)


def register_success(request):
    return render(request, REGISTER_SUCCESSFUL_HTML)


@login_required
def decks(request):
    decks = [deck.deck for deck in DeckUser.objects.filter(user=request.user)]

    for deck in decks:
        deck.card_count = Card.objects.filter(deck=deck).count()

    context = {
        'decks': decks
    }

    return render(request, DECKS_HTML, context)


@login_required
def decks_create(request):
    if request.method == HTTP_POST:
        name = request.POST.get('name')
        private = True if request.POST.get('private') == 'yes' else False

        deck = Deck.objects.create(
            name=name,
            private=private
        )

        deck_user = DeckUser.objects.create(
            deck=deck,
            user=request.user,
            role_cd='O'
        )

        Settings.initialize(deck_user)

        return HttpResponseRedirect(reverse(DECKS_URL))

    return render(request, DECKS_CREATE_HTML)


@login_required
def decks_delete_confirm(request, deck_id):
    context = {
        'deck': Deck.objects.get(deck_id=deck_id)
    }

    return render(request, DECKS_DELETE_CONFIRM_HTML, context)


@login_required
def decks_delete(request, deck_id):
    Deck.objects.get(deck_id=deck_id).delete()
    return HttpResponseRedirect(reverse(DECKS_URL))


@login_required
def decks_edit(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)
    cards = Card.objects.filter(deck=deck)

    if request.method == HTTP_POST:
        deck.name = request.POST.get('name')
        deck.private = True if request.POST.get('private') == 'yes' else False
        deck.save()

    context = {
        'deck': deck,
        'cards': cards,
        'first_card': cards[0] if len(cards) > 0 is not None else None
    }

    return render(request, DECKS_EDIT_HTML, context)


@login_required
def cards_add(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)

    if request.method == HTTP_POST:
        card = Card.objects.create(
            deck=deck,
            front=request.POST.get('front'),
            back=request.POST.get('back')
        )

        tags = split_comma_separated_into_list(request.POST.get('tags'))
        CardTag.create_from_list(card, tags)

        return HttpResponseRedirect(reverse(DECKS_EDIT_URL, args=(deck_id,)))
    
    context = {
        'deck': deck
    }

    return render(request, CARDS_ADD_HTML, context)


@login_required
def cards_edit(request, deck_id, card_id):
    deck = Deck.objects.get(deck_id=deck_id)
    card = Card.objects.get(card_id=card_id)
    tags = CardTag.objects.filter(card=card)

    if request.method == HTTP_POST:
        card.update(
            front=request.POST.get('front'),
            back=request.POST.get('back')
        )

        # Reset all tags for the card
        CardTag.objects.filter(card=card).delete()

        tags = split_comma_separated_into_list(request.POST.get('tags'))
        CardTag.create_from_list(card, tags)

        return HttpResponseRedirect(reverse(DECKS_EDIT_URL, args=(deck_id,)))

    context = {
        'deck': deck,
        'card': card,
        'tags_string': ','.join([tag.tag for tag in tags])
    }

    return render(request, CARDS_EDIT_HTML, context)


@login_required
def cards_delete(request, deck_id, card_id):
    deck = Deck.objects.get(deck_id=deck_id)
    card = Card.objects.get(card_id=card_id)

    if request.method == HTTP_POST:
        card.delete()
        return HttpResponseRedirect(reverse(DECKS_EDIT_URL, args=(deck_id,)))

    context = {
        'deck': deck,
        'card': card
    }

    return render(request, CARDS_DELETE_CONFIRM_HTML, context)


@login_required
def cards_delete_all(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)

    if request.method == HTTP_POST:
        cards = Card.objects.filter(deck=deck)
        cards.delete()

        return HttpResponseRedirect(reverse(DECKS_EDIT_URL, args=(deck_id,)))

    context = {
        'deck': deck
    }
    
    return render(request, CARDS_DELETE_ALL_HTML, context)

@login_required
def cards_import(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)

    if request.method == HTTP_POST:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage()
        filename = fs.save(upload_file.name, upload_file)
        uploaded_file_url = fs.url(filename)

        deck.import_cards_from_file(filename)
        
        return HttpResponseRedirect(reverse(DECKS_EDIT_URL, args=(deck_id,)))

    context = {
        'deck': deck,
    }

    return render(request, CARDS_IMPORT_HTML, context)


@login_required
def review_start(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)
    tags = CardTag.objects.filter(card__deck=deck).values('tag')
    tags_sorted = list(set([x['tag'] for x in list(tags)]))
    tags_sorted.sort()

    context = {
        'deck': deck,
        'tags': tags_sorted
    }

    deck_user = DeckUser.objects.get(deck=deck, user=request.user)
    settings = Settings.objects.filter(deck_user=deck_user)

    if request.method == HTTP_POST:
        selected_tags = ','.join(request.POST.getlist('tags'))

        settings.filter(setting='TAGS').delete()

        Settings.objects.create(
            deck_user=deck_user,
            setting='TAGS',
            value=selected_tags
        )

        question_side = request.POST.get('question_side')
        question_side_setting = settings.get(setting='QUESTION_SIDE')
        question_side_setting.value = question_side
        question_side_setting.save()

        shuffle = request.POST.get('shuffle')
        shuffle_setting = settings.get(setting='SHUFFLE')
        shuffle_setting.value = shuffle
        shuffle_setting.save()

    tags_setting = settings.get(setting='TAGS')
    context['selected_tags'] = split_comma_separated_into_list(tags_setting.value)

    question_side_setting = settings.get(setting='QUESTION_SIDE')
    context['question_side'] = question_side_setting.value

    shuffle_setting = settings.get(setting='SHUFFLE')
    context['shuffle'] = shuffle_setting.value

    return render(request, REVIEW_START_HTML, context)


@login_required
def review(request, deck_id):
    deck = Deck.objects.get(deck_id=deck_id)
    deck_user = DeckUser.objects.get(deck=deck, user=request.user)
    settings = Settings.objects.filter(deck_user=deck_user)

    cards = Card.objects.filter(deck=deck)
    review_items = []

    for card in cards:
        selected_tags = split_comma_separated_into_list(settings.get(setting='TAGS').value)
        tags = [tag.tag for tag in CardTag.objects.filter(card=card)]

        if len(set(selected_tags).intersection(set(tags))) == 0:
            continue

        review = Review.objects.filter(card=card, user=request.user)
        add_card = True

        if review.exists():
            review = review[0]

            if not review.review_today():
                add_card = False
        
        if add_card:
            review_item = {'cardId': card.card_id}

            if settings.get(setting='QUESTION_SIDE') == 'FRONT':
                review_item['question'] = card.front
                review_item['answer'] = card.back
            else:
                review_item['question'] = card.back
                review_item['answer'] = card.front

            review_items.append(review_item)
    
    if len(review_items) == 0:
        return HttpResponseRedirect(reverse(REVIEW_END_URL, args=(deck_id,)))

    if settings.get(setting='SHUFFLE').value == 'TRUE':
        shuffle(review_items)

    context = {
        'deck': deck,
        'review_items': review_items
    }

    return render(request, REVIEW_HTML, context)


@login_required
def review_assessment(request, deck_id):
    review_items = json.loads(request.GET.get('reviewItems'))

    for item in review_items:
        time_to_answer = item['timeToAnswer']

        if time_to_answer < 7:
            status_cd = 'EASY'
            days_to_add = 7
        elif time_to_answer < 10:
            status_cd = 'MODERATE'
            days_to_add = 3
        else:
            status_cd = 'HARD'
            days_to_add = 1

        date_to_review = datetime.datetime.today() + datetime.timedelta(days=days_to_add)

        review = Review.objects.filter(card_id=item['cardId'], user=request.user)

        if review:
            review = review[0]
            review.status_cd = status_cd
            review.date_to_review = date_to_review
            review.save()
        else:
            Review.objects.create(
                card=Card.objects.get(card_id=item['cardId']),
                user=request.user,
                status_cd=status_cd,
                date_to_review=date_to_review
            )
    
    return JsonResponse({'hello': True})


@login_required
def review_end(request, deck_id):
    return render(request, REVIEW_END_HTML)
