# Generated by Django 3.0.5 on 2020-08-15 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('idCountry', models.IntegerField(primary_key=True, serialize=False)),
                ('a2Code', models.CharField(db_column='A2', default='', max_length=2, null=True)),
                ('a3Code', models.CharField(db_column='A3', default='', max_length=3, null=True)),
                ('countryName', models.CharField(db_column='countryName', max_length=50)),
                ('phonePrefix', models.IntegerField(db_column='PhonePrefix', default=0, null=True)),
                ('idFlag', models.IntegerField(default=0, null=True)),
            ],
            options={
                'db_table': 'Country',
                'ordering': ['countryName'],
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('idRestaurant', models.AutoField(primary_key=True, serialize=False)),
                ('restaurantName', models.CharField(db_column='GroupName', max_length=250)),
                ('address1', models.CharField(db_column='Address1', max_length=100)),
                ('address2', models.CharField(db_column='Address2', default='', max_length=100, null=True)),
                ('address3', models.CharField(db_column='Address3', default='', max_length=100, null=True)),
                ('city', models.CharField(db_column='City', max_length=50)),
                ('postcode', models.CharField(db_column='PostCode', default='', max_length=20, null=True)),
                ('phones', django_mysql.models.JSONField(db_column='phones', default=dict)),
                ('email', models.CharField(db_column='Email', default='', max_length=255, null=True)),
                ('website', models.CharField(db_column='Website', default='', max_length=50, null=True)),
                ('vatNumber', models.CharField(db_column='VATNumber', default='', max_length=20, null=True)),
                ('currency', models.CharField(db_column='Currency', default='', max_length=20, null=True)),
                ('openingTime', models.TimeField(db_column='OpeningTime')),
                ('closingTime', models.TimeField(db_column='ClosingTime')),
                ('latitude', models.DecimalField(db_column='Latitude', decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(db_column='Longitude', decimal_places=6, max_digits=9)),
                ('country', models.ForeignKey(db_column='idCountry', on_delete=django.db.models.deletion.CASCADE, to='services.Country')),
            ],
            options={
                'db_table': 'Restaurant',
                'ordering': ['restaurantName'],
            },
        ),
        migrations.CreateModel(
            name='UserFavoriteRestaurant',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('idUserFavorite', models.AutoField(primary_key=True, serialize=False)),
                ('restaurant', models.ForeignKey(db_column='idRestaurant', on_delete=django.db.models.deletion.CASCADE, to='services.Restaurant')),
                ('user', models.ForeignKey(db_column='iduser', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserFavoriteRestaurants',
            },
        ),
        migrations.CreateModel(
            name='UserBlocklistRestaurant',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('idUserBlocklist', models.AutoField(primary_key=True, serialize=False)),
                ('restaurant', models.ForeignKey(db_column='idRestaurant', on_delete=django.db.models.deletion.CASCADE, to='services.Restaurant')),
                ('user', models.ForeignKey(db_column='iduser', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserBlocklistRestaurants',
            },
        ),
    ]
