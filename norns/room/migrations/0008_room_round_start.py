# Generated by Django 2.0.5 on 2018-05-24 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0007_auto_20180522_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='round_start',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
