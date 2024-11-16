# Generated by Django 5.1.3 on 2024-11-16 03:52

import django.db.models.deletion
import features.property_management.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('boarding_room', 'Boarding Room')], default='boarding_room', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BoardingHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('barangay', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.barangay')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('municipality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.municipality')),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.province')),
            ],
        ),
        migrations.CreateModel(
            name='BoardingHouseImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=features.property_management.models.boarding_house_image_path)),
                ('boarding_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='property_management.boardinghouse')),
            ],
        ),
        migrations.CreateModel(
            name='BoardingRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(max_length=2000)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('boarding_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='property_management.boardinghouse')),
            ],
        ),
        migrations.CreateModel(
            name='BoardingRoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=features.property_management.models.boarding_room_image_path)),
                ('boarding_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='property_management.boardingroom')),
            ],
        ),
        migrations.CreateModel(
            name='BoardingRoomTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boarding_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='property_management.boardingroom')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_management.tag')),
            ],
        ),
    ]
