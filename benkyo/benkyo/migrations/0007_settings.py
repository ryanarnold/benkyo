# Generated by Django 2.0.7 on 2018-08-11 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benkyo', '0006_auto_20180805_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting', models.CharField(choices=[('TAGS', 'TAGS'), ('DIRECTION', 'DIRECTION')], max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('deck_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benkyo.DeckUser')),
            ],
        ),
    ]
