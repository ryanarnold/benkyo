# Generated by Django 2.0.7 on 2018-07-29 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benkyo', '0003_auto_20180729_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('card_id', models.AutoField(primary_key=True, serialize=False)),
                ('front', models.CharField(max_length=100)),
                ('back', models.CharField(max_length=100)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benkyo.Deck')),
            ],
        ),
        migrations.CreateModel(
            name='CardTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benkyo.Card')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cardtag',
            unique_together={('card', 'tag')},
        ),
    ]
