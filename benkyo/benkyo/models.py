from os import path

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import (CASCADE, SET_NULL, AutoField, BooleanField, CharField,
                              ForeignKey, Model, DateField, TextField)
from django.core.exceptions import ObjectDoesNotExist
from openpyxl import load_workbook


class Deck(Model):
    deck_id = AutoField(primary_key=True)
    name = CharField(max_length=100)

    def import_cards_from_file(self, filename):
        workbook = load_workbook(path.join(settings.MEDIA_ROOT, filename))
        sheet = workbook.active

        row = 2
        while True:
            # front = sheet['A' + str(row)].value

            # if front == None:
            #     break

            # back = sheet['B' + str(row)].value
            # category = sheet['C' + str(row)].value

            kana =  sheet['A' + str(row)].value
            kanji = sheet['B' + str(row)].value
            english = sheet['C' + str(row)].value
            category = sheet['D' + str(row)].value

            # Break once you reach a blank record
            if kana is None:
                break

            # Automatically create a category if it does not yet exist
            try:
                category = Category.objects.get(pk=category)
            except ObjectDoesNotExist:
                category = Category.objects.create(category_cd=category)
            
            if (kanji is None):
                card = Card.objects.create(
                    deck=self,
                    front=kana,
                    back=english,
                    category=category,
                    info=kana
                )
            else:
                card = Card.objects.create(
                    deck=self,
                    front=kanji,
                    back=english,
                    category=category,
                    info=''
                )

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


class Settings(Model):
    settings = (
        ('TAGS', 'TAGS'),
        ('QUESTION_SIDE', 'QUESTION_SIDE'),
        ('SHUFFLE', 'SHUFFLE'),
        ('START_INDEX', 'START_INDEX'),
        ('END_INDEX', 'END_INDEX'),
    )

    REVIEW_TYPE = 'QUESTION_SIDE'

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
            setting='REVIEW_TYPE',
            value='RECOGNIZE'
        )
