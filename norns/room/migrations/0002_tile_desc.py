# Generated by Django 2.0.5 on 2018-05-21 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tile',
            name='desc',
            field=models.TextField(blank=True),
        ),
    ]
