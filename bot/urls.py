from django.urls import path
from .views import GetAllPlaces, UserRegistration, CustomAuthToken, CheckAuth

urlpatterns = [
    path('places', GetAllPlaces.as_view()),
    path('register', UserRegistration.as_view()),
    path('token', CustomAuthToken.as_view()),
    path('checkAuth', CheckAuth.as_view()),
]