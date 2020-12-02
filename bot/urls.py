from django.urls import path
from .views import UserSignup, GetAllPlaces, UserLogin, Followers

urlpatterns = [
    path('places/', GetAllPlaces.as_view()),
    path('users/', UserSignup.as_view()),
    path('login/', UserLogin.as_view()),
    path('follow/', Followers.as_view())
]