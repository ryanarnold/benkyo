from django.db.models import Model
from django.db.models import CharField, AutoField, BooleanField, ForeignKey
from django.db.models import CASCADE
from django.contrib.auth.models import User


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
