# python
from __future__ import unicode_literals
# libs
from utils.controllers import ControllerBase
from utils.exceptions import ServiceValidationError
# local
from ..models import Restaurant


class RestaurantListController(ControllerBase):

    class Meta:
        model = Restaurant
        default_list_limit = 50
        max_list_limit = 100
        allowed_ordering = ['idRestaurant', 'restaurantName', 'city', 'postcode']
        search_fields = {
            'idRestaurant': ('in', 'gt', 'lt', 'gte', 'lte', 'range'),
            'restaurantName': ('in', 'isnull', 'icontains', 'istartswith',
                               'iendswith'),
            'city': ('in', 'isnull', 'icontains', 'istartswith',
                            'iendswith'),
            'postcode': ('in', 'isnull', 'icontains', 'istartswith',
                            'iendswith'),
        }
        validation_order = ('search', 'exclude', 'limit', 'page', 'order')
        error_class = 'Restaurant List Errors'