# python
from __future__ import unicode_literals
import datetime
import json
import re
# libs
from dateutil import parser
# from utils import exception_codes_for_method
# local
from .exceptions import *


REMOVE_PATTERN = "[\[\]()\'\"]"


class ControllerBase():
    """Base controller class for all controllers. it contains basic methods
    and attributes valid for all controllers.
    """

    class Meta:
        """REST Controllers migrate their config data into this Meta class

        :attribute default_list_limit: if limit is not passed in request, this
                                       value will be used as default
        :type default_list_limit: int
        :attribute max_list_limit: specifies a maximum number of items that
                                   list can return, if limit is greater than
                                   max_list_limit, max_list_limit will be used
                                   instead
        :type max_list_limit: int
        :attribute model: Model class that ControllerBase should operate on
                          if given, controller will be able to create/update
                          instances of that class
        :attribute: django.db.models.Model
        :attribute validation_order: order in which .is_valid() should execute
                                     validation process
        :type validation_order: list
        :attribute search_fields: dict of allowed search fields mapped against
                                  their available lookup operators
        :type search_fields: dict
        :attribute allowed_ordering: list of allowed ordering fields as
                                     specified in model.
        :type allowed_ordering: list

        """
        error_class = None
        default_list_limit = 50
        max_list_limit = 100
        model = None
        search_fields = dict()
        validation_order = list()
        allowed_ordering = list()

    def __init__(self, request=None, instance=None, data=None, partial=False):
        """Initializes new object.

        :param request: Django wsgi request instance
        :type request: Request
        """
        self.operators = ['in', 'isnull', 'icontains', 'istartswith',
                          'iendswith', 'iexact', 'gt', 'lt', 'gte', 'lte',
                          'range', 'year', 'month', 'day', 'week_day',
                          'hour', 'minute']
        self.request = request
        self.user = request.user
        self.cleaned_data = dict()
        self._errors = dict()
        self.kwargs = dict()
        self.partial = partial
        self._instance = instance
        self._meta = self.Meta()
        self.data = data
        if getattr(self._meta, 'model', None):
            self.get_field = self._meta.model._meta.get_field

    def validate_page(self, page):
        """Validates page to ensure it's positive int.

        :param page: page number
        :type page: int
        """
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 0
        if page < 0:
            page = 0
        self.cleaned_data['page'] = page

    def validate_limit(self, limit):
        """Validates limit to ensure it's positive int.

        :param limit: amount of records to return in the call
        :type limit: int
        """
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = self._meta.default_list_limit
        max_limit = self._meta.max_list_limit
        if limit <= 0 or limit > max_limit:
            limit = self._meta.default_list_limit
        self.cleaned_data['limit'] = limit

    def validate_order(self, order, replaceable=None):
        if not order:
            self.cleaned_data['order'] = self._meta.allowed_ordering[0]
            return
        replaceable = replaceable or dict()
        ord_dir = "" if order.lstrip("-") != order else "-"
        if order.lstrip('-') in self._meta.allowed_ordering:
            if order.lstrip('-') in replaceable.keys():
                order = "%s%s" % (ord_dir, replaceable[order])
            self.cleaned_data['order'] = order
            return
        self.cleaned_data['order'] = self._meta.allowed_ordering[0]

    def validate_search(self, *args):
        """Validate search doesn't validate the value that it receives from
        is_valid method. Since the fields it needs to validate are specified
        if controller Meta class it picks up correct values from self.data
        and filters out what should be validated and populates
        self.cleaned_data['search'] with a set of kwargs that should be passed
        directly to the queryset.

        :param args: list of arguments (ignored)
        :type args: list
        """
        search = dict()

        for q, val in self.data.items():
            # check that q is one of the allowed search values and if it
            # contains and operator split it into field and operator
            q = q.split("__")
            op = None
            if len(q) > 1 and q[-1] in self.operators:
                op = q[-1]
                q = q[:-1]
            q = "__".join(q)
            allowed_ops = self._meta.search_fields.get(q, None)
            if allowed_ops is None or (allowed_ops is () and op) or \
                    (op and op not in allowed_ops):
                continue

            # special handling for values that are not standard:
            #   isnull - bool
            #   in - iterable
            #   range - iterable with 2 items
            #   year, month, day, week_day, hour, minute - int
            if op in ['in', 'range']:
                if isinstance(val, list):
                    val = val[0]

                val = re.sub(REMOVE_PATTERN, "", val).split(",")
                val = filter(None, (v.strip() for v in val))
                if op == 'range' and len(list(val)) > 2:
                    continue
            elif op == 'isnull' or val in ['true', 'false']:
                val = True if val == 'true' else False
            elif op in ['year', 'month', 'day', 'week_day', 'hour', 'minute']:
                try:
                    val = int(val)
                except ValueError:
                    continue

            search["__".join(filter(None, [q, op]))] = val
        self.cleaned_data['search'] = search

    def validate_exclude(self, *args):
        pre_exclude = ((k.replace('exclude__', ''), v)
                       for k, v in self.data.items()
                       if k.startswith('exclude__'))
        exclude = dict()
        for q, val in pre_exclude:
            # check that q is one of the allowed search values and if it
            # contains and operator split it into field and operator
            q = q.split("__")
            op = None
            if q[-1] in self.operators:
                op = q[-1]
                q = q[:-1]
            q = "__".join(q)
            allowed_ops = self._meta.search_fields.get(q, None)
            if allowed_ops is None or (allowed_ops is () and op) or \
                    (op and op not in allowed_ops):
                continue

            # special handling for values that are not standard:
            #   isnull - bool
            #   in - iterable
            #   range - iterable with 2 items
            #   year, month, day, week_day, hour, minute - int
            if op in ['in', 'range']:
                if isinstance(val, list):
                    val = val[0]

                val = re.sub(REMOVE_PATTERN, "", val).split(",")
                val = filter(None, (v.strip() for v in val))
                if op == 'range' and len(list(val)) > 2:
                    continue
            elif op == 'isnull' or val in ['true', 'false']:
                val = True if val == 'true' else False
            elif op in ['year', 'month', 'day', 'week_day', 'hour', 'minute']:
                try:
                    val = int(val)
                except ValueError:
                    continue

            exclude["__".join(filter(None, [q, op]))] = val
        self.cleaned_data['exclude'] = exclude

    def is_valid(self):
        for field in self._meta.validation_order:
            try:
                m = getattr(self, 'validate_%s' % field, None)
                if not m:
                    continue
                if self.partial and field not in self.data:
                    continue
                data_val = self.data.get(field)
                if isinstance(data_val, str):
                    data_val = data_val.strip()
                m(data_val)
            except ServiceValidationError as e:
                self._errors[field] = self._errors.get(field) or list()
                self._errors[field].append(e.error_code)

        return not bool(self._errors)

    @property
    def instance(self):
        local_fields = [f.name for f in self._meta.model._meta.fields]
        if self._instance and self.cleaned_data:
            for k, v in self.cleaned_data.items():
                if k in local_fields:
                    setattr(self._instance, k, v)
            return self._instance
        if self._instance:
            return self._instance
        if self._meta.model and not self._instance and \
                self.cleaned_data and not self._errors:
            self._instance = self._meta.model(**self.cleaned_data)
            return self._instance
        raise AttributeError('You need to specify the Controller.model and '
                             'you need to validate the controller data')

    def has_error(self, key):
        return key in self._errors

    @property
    def errors(self):
        if not self._meta.error_class:
            return self._errors

        _errors = dict()
        for k, v in self._errors.items():
            _errors[k] = v[0]
        return _errors
