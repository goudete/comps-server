from django.contrib.auth.models import User
from friendship.models import Follow
from django.contrib.auth import authenticate
from .models import Place, Ratings
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
from recommender.recommend import Recommend


class UserSignup(APIView):
    """
    Create a new user & retrieving a list of all User objects.
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

    # get all users
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        usrname = request.data.get('username')
        pword = request.data.get('password')

        usr = authenticate(username=usrname, password=pword)
        if usr:
            token, created = Token.objects.get_or_create(user = usr)
            return Response({
                'token': token.key,
                'username': usr.username,
                'user_id': usr.id
            })
        return Response('Login credentials incorrect')


# This is working - leave for now
class GetAllPlaces(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        places = [places for places in Place.objects.all()]
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


class Followers(APIView):
    # Creates a follow relationship between two users
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id = request.data.get('user_id'))
        other_user = User.objects.get(id = request.data.get('other_user_id'))
        try:
            #Create follow relationship
            Follow.objects.add_follower(user, other_user)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #Return a user's followers & following
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id = request.data.get('user_id'))
        response_dict = {}
        followers_arr = []
        following_arr = []
        try:
            # Query database
            followers = Follow.objects.followers(user)
            following = Follow.objects.following(user)

            # Get size of followers and following
            response_dict['follower_count'] = len(followers)
            response_dict['following_count'] = len(following)

            #Handles followers
            for follow in followers:
                # Query db to get user object
                follow_user_object = User.objects.get(username=follow)
                user_id = follow_user_object.id
                username = follow_user_object.username
                followers_arr.append({'user_id': user_id, 'username': username})
            response_dict['followers'] = followers_arr
            
            #Handles following
            for f in following:
                following_user_object = User.objects.get(username=f)
                user_id = following_user_object.id
                username = following_user_object.username
                following_arr.append({'user_id': user_id, 'username': username})
            response_dict['following'] = following_arr

            return Response(response_dict, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        '''
        Response object shape
        {   
            'follower_count': <number_of_followers>,
            'following_count': <number_of_following>,
            'followers': [
                {
                    'user_id': '<id>',
                    'username': '<username>'
                }
            ],
            'following': [
                {
                    'user_id': '<id>',
                    'username': '<username>'
                }
            ]      
        }   
        '''


class Recommender(APIView):

    def post(self, request, *args, **kwargs):
        ratings = Ratings.objects.all()
        ratings_data = []
        for r in ratings:
            ratings_data.append([r.user.id, r.place.id, r.rating])

        #instantiating Recommend class
        recommender = Recommend()

        #plug in user_id
        recommender_res = recommender.get_user_recs(ratings_data, 9)
        response_dict = {}
        recommendations = []
        for rec in recommender_res:
            place = Place.objects.get(id=rec)
            name = place.name
            address = place.address

            recommendations.append({
                'place_id': place.id, 
                'name': place.name,
                'address': place.address,
                'tag': place.tag,
                'neighborhood': place.neighborhood,
                'instagram': place.instagram
            })
        response_dict['recommendations'] = recommendations

        return Response(response_dict, status=status.HTTP_200_OK)


        '''
            Response object shape
            {   
            'recommendations': [
                {
                    'place_id': '<id>',
                    'name': '<name>',
                    'address': '<address>',
                    'tag': '<tag>',
                    'neighborhood': '<neighborhood>',
                    'instagram': '<instagram>'
                }
            ]
            }   
        '''