from django.contrib.auth.models import User
from .models import Place
from .serializers import UserSerializer, PlaceSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, permissions, status, mixins, generics, authentication, exceptions
from rest_framework.permissions import IsAuthenticated
import json
import googlemaps


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """
    serializer = UserSerializer

    # create new user (called on signup)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            usr = serializer.save()
            token, created = Token.objects.get_or_create(user=usr)
            return Response({
                'token': token.key,
                'username': usr.username,
                'user_id': usr.id,
                })
        return Response(serializer.errors)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# This is working - leave for now
class GetAllPlaces(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        places = [places for places in Place.objects.all()]
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)



# def createPlace(request, ):
#     #takes address and gets coords
#     gmaps=googlemaps.Client(key='AIzaSyAftwrvS2Mphv821bXwZMOR3EmC6esH8Fk')
#     coords = gmaps.geocode(request.placeAddress)


# def makeFriendship()

# def sendFriendRequest()

# def respondFriendRequest()

# def etc...