# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-20 20:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('create_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_start_date', models.DateTimeField()),
                ('booking_end_date', models.DateTimeField()),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banner.Banner')),
            ],
        ),
        migrations.CreateModel(
            name='PricePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=15)),
                ('price_start_date', models.DateTimeField()),
                ('price_end_date', models.DateTimeField()),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banner.Banner')),
            ],
        ),
    ]
