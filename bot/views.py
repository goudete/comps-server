from django.contrib.auth.models import User
from .models import Place

from .serializers import UserSerializer, UserSerializerWithToken, PlaceSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, permissions, status, mixins, generics, authentication, exceptions
import json


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllPlaces(APIView):
    def get(self, request, *args, **kwargs):
        places = [places for places in Place.objects.all()]
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

