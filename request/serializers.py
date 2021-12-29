from .models import Request
from rest_framework import serializers

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id','sender','receiver','added_date']
    def create(self, validated_data):
        return Request.objects.create(**validated_data)