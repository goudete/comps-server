from django.urls import path
from .views import UserList, GetAllPlaces

urlpatterns = [
    path('places/', GetAllPlaces.as_view()),
    path('users/', UserList.as_view()),
    #path('friendship/', friendship.urls)
]