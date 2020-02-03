from os import path
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import (CASCADE, SET_NULL, AutoField, BooleanField, CharField,
                              ForeignKey, Model, DateField, TextField)
from openpyxl import load_workbook


class Deck(Model):
    deck_id = AutoField(primary_key=True)
    name = CharField(max_length=100)

    def import_cards_from_file(self, filename):
        workbook = load_workbook(path.join(settings.MEDIA_ROOT, filename))
        sheet = workbook['MAIN']

        row = 2
        while True:
            front = sheet['A' + str(row)].value

            if front == None:
                break

            back = sheet['B' + str(row)].value
            category = sheet['C' + str(row)].value

            card = Card.objects.create(
                deck=self,
                front=front,
                back=back
            )

            card.category_cd = Card.objects.get(pk=category)

            row += 1


class DeckUser(Model):
    roles = (
        ('OWNER', 'OWNER'),
        ('USER', 'USER')
    )

    deck = ForeignKey(Deck, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    role_cd = CharField(max_length=50, choices=roles)

    class Meta:
        unique_together = (('deck', 'user', 'role_cd'),)


class Category(Model):
    category_cd = CharField(max_length=100, primary_key=True)


class Card(Model):
    card_id = AutoField(primary_key=True)
    deck = ForeignKey(Deck, on_delete=CASCADE)
    front = CharField(max_length=100)
    back = CharField(max_length=100)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)
    info = TextField(max_length=1000, null=True)

    def update(self, front, back):
        self.front = front
        self.back = back
        self.save()



class Review(Model):
    status = (
        ('UNKNOWN', 'UNKNOWN'),
        ('SEEN', 'SEEN'),
        ('FAMILIAR', 'FAMILIAR'),
        ('KNOWN', 'KNOWN')
    )

    card = ForeignKey(Card, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    status_cd = CharField(max_length=50, choices=status)

    class Meta:
        unique_together = (('card', 'user'),)
    
    def review_today(self):
        if datetime.datetime.today().date() >= self.date_to_review:
            return True
        else:
            return False


class Settings(Model):
    settings = (
        ('TAGS', 'TAGS'),
        ('QUESTION_SIDE', 'QUESTION_SIDE'),
        ('SHUFFLE', 'SHUFFLE'),
        ('START_INDEX', 'START_INDEX'),
        ('END_INDEX', 'END_INDEX'),
    )

    TAGS = 'TAGS'
    QUESTION_SIDE = 'QUESTION_SIDE'
    SHUFFLE = 'SHUFFLE'
    START_INDEX = 'START_INDEX'
    END_INDEX = 'END_INDEX'
    FORMAT = 'FORMAT'
    LIMIT = 'LIMIT'

    deck_user = ForeignKey(DeckUser, on_delete=CASCADE)
    setting = CharField(max_length=100, choices=settings)
    value = CharField(max_length=100)

    @staticmethod
    def initialize(deck_user):
        Settings.objects.create(
            deck_user=deck_user,
            setting='TAGS',
            value=''
        )

        Settings.objects.create(
            deck_user=deck_user,
            setting='QUESTION_SIDE',
            value='FRONT'
        )

        Settings.objects.create(
            deck_user=deck_user,
            setting='SHUFFLE',
            value='FALSE'
        )

        Settings.objects.create(
            deck_user=deck_user,
            setting='START_INDEX',
            value='1'
        )

        Settings.objects.create(
            deck_user=deck_user,
            setting='END_INDEX',
            value='1'
        )

        Settings.objects.create(
            deck_user=deck_user,
            setting='FORMAT',
            value='CHOICE'
        )

        Settings.objects.create(
            deck_user=deck_user,
            setting='LIMIT',
            value='50'
        )
