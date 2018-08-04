from django.contrib.auth.models import User
from django.db.models import (CASCADE, AutoField, BooleanField, CharField,
                              ForeignKey, Model)
from django.conf import settings
from os import path
from openpyxl import load_workbook



class Deck(Model):
    deck_id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    private = BooleanField()

    def import_cards_from_file(self, filename):
        workbook = load_workbook(path.join(settings.MEDIA_ROOT, filename))
        sheet = workbook['MAIN']

        row = 2
        while True:
            front = sheet['A' + str(row)].value

            if front == None:
                break

            back = sheet['B' + str(row)].value
            tags = sheet['C' + str(row)].value.split(',')

            card = Card.objects.create(
                deck=self,
                front=front,
                back=back
            )

            for tag in tags:
                CardTag.objects.create(
                    card=card,
                    tag=tag
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


class Card(Model):
    card_id = AutoField(primary_key=True)
    deck = ForeignKey(Deck, on_delete=CASCADE)
    front = CharField(max_length=100)
    back = CharField(max_length=100)


class CardTag(Model):
    card = ForeignKey(Card, on_delete=CASCADE)
    tag = CharField(max_length=100)

    class Meta:
        unique_together = (('card', 'tag'),)
