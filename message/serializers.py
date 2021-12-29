from .models import Message
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','userSrc','userDst','content','seen','added_date']
    def create(self, validated_data):
        return Message.objects.create(**validated_data)