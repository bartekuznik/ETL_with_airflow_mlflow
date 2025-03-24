from django.urls import path
from .views import get_all_data, get_lastets, post_data

urlpatterns = [
    path('all/', get_all_data, name='get_all_data'),
    path('last/', get_lastets, name='get_lastets'),
    path('add/', post_data, name="post_data")
]