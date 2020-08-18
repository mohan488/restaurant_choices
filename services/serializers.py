# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from . import models


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = ('idCountry', 'a2Code', 'a3Code', 'countryName',
                  'phonePrefix', 'idFlag', 'created', 'updated')
        read_only_fields = ('created', 'updated')


class RestaurantSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    distance = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Restaurant
        fields = ('idRestaurant','country', 'restaurantName','address1',
                  'address2', 'address3', 'city', 'postcode', 'phones',
                  'email', 'website', 'vatNumber',  'currency', 'distance',
                  'status', 'created', 'updated')
        read_only_fields = ('country', 'distance', 'status', 'created', 
                            'updated')

    def get_distance(self, obj):
        return obj.distance
    
    def get_status(self, obj):
        return obj.status