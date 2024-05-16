from django.urls import path
from .views import *

urlpatterns = [
    path('', weather_api_post_method)
]