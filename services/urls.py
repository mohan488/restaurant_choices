from django.urls import path
from .views import restaurant

app_name = "services"
urlpatterns = [
    path("v1/restaurant/",
         view=restaurant.RestaurantCollection.as_view(),
         name="restaurant_collection"),

]
