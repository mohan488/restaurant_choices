# python
from __future__ import unicode_literals
from datetime import datetime, time
from math import radians, cos, sin, asin, sqrt
from decimal import Decimal
# libs
import coreapi
import coreschema
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import schemas
# local
from utils import exceptions
from ..models import (Country, Restaurant, UserFavoriteRestaurant,
                      UserBlocklistRestaurant)
from ..controllers.restaurant import RestaurantListController
from ..serializers import RestaurantSerializer


def status_distance(userData, object):
    """ helper function for RestaurantCollection
    retuns distance btween user and restaurant, 
    currently open status """

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [Decimal(userData.GET['longitude']),
                                          Decimal(userData.GET['latitude']),
                                           object.longitude, object.latitude])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    miles =  '%0.1f Miles' %(6371 * c  * 0.62137)

    # to check restaurant currently open
    if object.openingTime < object.closingTime:
        status =  datetime.utcnow().time() >= object.openingTime and\
                   datetime.utcnow().time() <= object.closingTime
    else: #Over midnight
        status =  datetime.utcnow().time() >= object.openingTime or\
                   datetime.utcnow().time() <= object.closingTime
    if status:
        status = 'Open now: Closes at ' +\
            str(object.closingTime.strftime( "%I:%M %p"))
    else:
        status = 'Closed  now: Opens at ' +\
            str(object.openingTime.strftime( "%I:%M %p"))

    return [miles, status]


class RestaurantCollection(APIView):

    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "user id",
            required=True,
            location="query",
            schema=coreschema.Integer()
        ),
        coreapi.Field(
            "longitude",
            required=True,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "latitude",
            required=True,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "country",
            required=False,
            location="query",
            schema=coreschema.Integer()
        ),
        coreapi.Field(
            "city",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "postcode",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "restaurant name",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
    ])
    
    def get(self, request, *args, **kwargs):

        """
        Get a list of all Restaurants. Based on Geographic location (eg., 
        country, city, postal code, restaurant name), supports all Django 
        Search options (eg., 'in', 'isnull', 'icontains', 'istartswith',
        'iendswith'). returns all favorite user restaurant including remaining 
        restaurant based search and ensures that Restaurant not blacklisted
        by user.

        serializer: .serializers.RestaurantSerializer
        omit_serializer: false
        many: true

        parameters_strategy: merge
        omit_parameters:
        - path

        parameters:
        - name: userId, example: 1
          required: true
          type: int
        - name: longitude, example: -2.172841
          required: true
          type: str
        - name: latitude, example: 57.149453
          required: true
          type: str
        - name: country, example: "United States"
          required: false
          type: str
        - name: city, example: "Aberdeen"
          required: false
          type: str
        - name: restaurantName__istartswith, example: "Aug"
          required: false
          type: str
        - name: postcode__iendswith, example: "1XZ"
          required: false
          type: str

        :returns: filtered restaurant based user search
        :rtype: json

    """

        controller = RestaurantListController(data=request.GET, request=request)
        controller.is_valid()
        kw = controller.cleaned_data['search']

        if "country" in request.GET:
            kw['country__countryName__contains'] = request.GET['country']
       
        try:
            objs = Restaurant.objects.filter(deleted__isnull=True, **kw)
        except (ValueError, ValidationError):
            raise exceptions.Http400(error_code='Restaurant List Error',
                                     errors ='check the search fields in parms'
                                    )

        favorite = UserFavoriteRestaurant.objects.filter(deleted__isnull=True, 
                                                         user = request.GET['userId']
                                                        ).values_list('restaurant', flat=True)
        blocklist = UserBlocklistRestaurant.objects.filter(deleted__isnull=True, 
                                                           user = request.GET['userId']
                                                        ).values_list('restaurant', flat=True)
        favoriteList, restaurants = [], []
        for obj in objs:
            if obj.idRestaurant in favorite:
                data = status_distance(request, obj)
                obj.distance, obj.status = data[0], data[1]
                favoriteList.append(obj)
            else:
                if obj.idRestaurant not in blocklist:
                    data = status_distance(request, obj)
                    obj.distance, obj.status = data[0], data[1]
                    restaurants.append(obj)

        page = controller.cleaned_data['page']
        limit = controller.cleaned_data['limit']
        metadata = {'page': page,
                    'limit': limit,
                    'order': controller.cleaned_data.get('order'),
                    'totalRecords': len(favoriteList + restaurants)}
        if controller.cleaned_data.get('order'):
            objs = objs.order_by(controller.cleaned_data['order'])
        objs = objs[page * limit:(page + 1) * limit]
        response = dict()
        response['content'] = {
                            'favoriteRestaurants': RestaurantSerializer(
                                                        instance=favoriteList,
                                                        many=True).data,
                            'restaurants': RestaurantSerializer(
                                                instance=restaurants,
                                                many=True).data}

        response['_metadata'] = metadata
        return Response(response)

