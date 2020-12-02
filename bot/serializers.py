from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from .models import Place
from rest_framework import serializers

#used by UserList class view POST method
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        usr = self.Meta.model(**validated_data)
        if password:
            usr.set_password(password)
        usr.email = email
        usr.save()
        return usr


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['name', 'address', 'tag', 'neighborhood', 'instagram', 'open_time', 'close_time']