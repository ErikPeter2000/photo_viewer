# Generated by Django 5.0.7 on 2024-07-19 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photographer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ImageReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField()),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo_viewer.photographer')),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField()),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo_viewer.photographer')),
            ],
        ),
    ]
