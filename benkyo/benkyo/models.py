from django.contrib.auth.models import User
from django.db.models import (CASCADE, AutoField, BooleanField, CharField,
                              ForeignKey, Model)


class Deck(Model):
    deck_id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    private = BooleanField()


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
