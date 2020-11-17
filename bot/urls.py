from django.urls import path
from .views import current_user, UserList, GetAllPlaces

urlpatterns = [
    path('places/', GetAllPlaces.as_view()),
    path('current_user/', current_user),
    path('users/', UserList.as_view())
]