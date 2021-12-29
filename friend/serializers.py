from .models import Friend, Request
from rest_framework import serializers
from user.serializers import UserSerializer
class FriendSerializer(serializers.ModelSerializer):
    friend1 = UserSerializer(many=True, read_only=True)
    friend2 = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Friend
        fields = ['id','friend1','friend2','added_date']