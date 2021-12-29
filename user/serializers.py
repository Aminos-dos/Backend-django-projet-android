from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','username','description','password','photo','phone','gender','email']
    def create(self, validated_data):
        return User.objects.create(**validated_data)