# Generated by Django 2.0.5 on 2018-05-22 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gear', '0006_auto_20180522_2102'),
        ('room', '0006_room_grid_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_south',
        ),
        migrations.RemoveField(
            model_name='room',
            name='room_west',
        ),
        migrations.AddField(
            model_name='tile',
            name='consumables',
            field=models.ManyToManyField(blank=True, to='gear.Consumable'),
        ),
        migrations.AddField(
            model_name='tile',
            name='weapons',
            field=models.ManyToManyField(blank=True, to='gear.Weapon'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_east',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_west', to='room.Room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_north',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_south', to='room.Room'),
        ),
        migrations.AlterField(
            model_name='tile',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.Room'),
        ),
    ]
