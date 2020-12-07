from django.urls import path
from .views import UserSignup, GetAllPlaces, UserLogin, Followers, Recommender, PlaceCoords, UserLists, AllUserLists

urlpatterns = [
    path('places/', GetAllPlaces.as_view()),
    path('users/', UserSignup.as_view()),
    path('login/', UserLogin.as_view()),
    path('follow/', Followers.as_view()),
    path('recommender/', Recommender.as_view()),
    path('coords/', PlaceCoords.as_view()),
    path('list/', UserLists.as_view()),
    path('all_lists/', AllUserLists.as_view())
]