# Generated by Django 2.0.7 on 2020-02-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benkyo', '0008_auto_20200203_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='setting',
            field=models.CharField(choices=[('REVIEW_TYPE', 'REVIEW_TYPE')], max_length=100),
        ),
    ]