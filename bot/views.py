from django.contrib.auth.models import User
from .models import Place

from .serializers import UserSerializer, PlaceSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, permissions, status, mixins, generics, authentication, exceptions
import json


# Create your views here.
class UserRegistration(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'id': user.id
            })
        else:
            raise exceptions.AuthenticationFailed("Invalid Data, please check again")

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CustomAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Password incorrect, please try again")

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id
        })

class CheckAuth(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            user = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("invalid user information, please login/register")
        
        return Response({
            "user": user.key
        })

# Figure out exactly how to write this function
class GetAllPlaces(APIView):
    def get(self, request, *args, **kwargs):
        places = [places for places in Place.objects.all()]
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

