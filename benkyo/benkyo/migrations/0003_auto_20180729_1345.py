# Generated by Django 2.0.7 on 2018-07-29 05:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('benkyo', '0002_auto_20180729_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deckuser',
            old_name='deck_id',
            new_name='deck',
        ),
        migrations.RenameField(
            model_name='deckuser',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='deckuser',
            name='role_cd',
            field=models.CharField(choices=[('OWNER', 'OWNER'), ('USER', 'USER')], max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='deckuser',
            unique_together={('deck', 'user', 'role_cd')},
        ),
    ]
