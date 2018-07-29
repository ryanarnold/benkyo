# Generated by Django 2.0.7 on 2018-07-29 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benkyo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deckuser',
            name='role_cd',
            field=models.CharField(choices=[('O', 'OWNER'), ('U', 'USER')], max_length=1),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
