# python
from __future__ import unicode_literals
# libs
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import JSONField

# Create your models here.

class TimeStampedModel(models.Model):
    '''
    DB structure to Tracking record created, updated and deleted 
    date, time.
    '''
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Country(TimeStampedModel):
    '''
    DB structure to store country information 
    Eg: UK, USA, ... 
    ''' 
    idCountry = models.IntegerField(primary_key=True)
    a2Code = models.CharField(db_column='A2', max_length=2, null=True, default='')
    a3Code = models.CharField(db_column='A3', max_length=3, null=True, default='')
    countryName = models.CharField(db_column='CountryName', max_length=50)
    phonePrefix = models.IntegerField(null=True, db_column='PhonePrefix', default=0)
    idFlag = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = 'Country'
        ordering = ['countryName']


class Restaurant(TimeStampedModel):
    '''
    DB structure to store restaurant information 
    ''' 
    idRestaurant = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, db_column='idCountry',
                                 on_delete=models.CASCADE)
    restaurantName = models.CharField(db_column='GroupName', max_length=250)
    address1 = models.CharField(db_column='Address1', max_length=100)
    address2 = models.CharField(null=True, db_column='Address2',
                                max_length=100, default='')
    address3 = models.CharField(null=True, db_column='Address3',
                                max_length=100, default='')
    city = models.CharField(db_column='City', max_length=50)
    postcode = models.CharField(null=True, db_column='PostCode',
                                max_length=20, default='')
    phones = JSONField(db_column='phones', default=dict)
    email = models.CharField(null=True, db_column='Email', max_length=255,
                             default='')
    website = models.CharField(null=True, db_column='Website', max_length=50,
                               default='')
    vatNumber = models.CharField(null=True, db_column='VATNumber',
                                 max_length=20, default='')
    currency = models.CharField(null=True, db_column='Currency',
                                 max_length=20, default='')
    openingTime = models.TimeField(db_column='OpeningTime')
    closingTime = models.TimeField(db_column='ClosingTime')
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   db_column='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    db_column='Longitude')

    class Meta:
        db_table = 'Restaurant'
        ordering = ['restaurantName']


class UserFavoriteRestaurant(TimeStampedModel):
    '''
    DB structure to store users favorite restaurants information 
    ''' 
    idUserFavorite = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, db_column='idRestaurant',
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='iduser',
                              on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'UserFavoriteRestaurants'


class UserBlocklistRestaurant(TimeStampedModel):
    '''
    DB structure to store users Blocklist restaurants information 
    ''' 
    idUserBlocklist = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, db_column='idRestaurant',
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='iduser',
                              on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'UserBlocklistRestaurants'



