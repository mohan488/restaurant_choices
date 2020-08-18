from django.contrib import admin
from services.models import *
from django.apps import apps

# Register your models here.
app = apps.get_app_config('services')
for model_name, model in app.models.items():
    admin.site.register(model)