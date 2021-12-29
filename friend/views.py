from django.shortcuts import render

from friend.models import Friend
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.decorators import api_view,permission_classes

@api_view(('DELETE',))
@permission_classes((permissions.AllowAny,))
def deleteFromFriend(request,id):
    try:
        friend = Friend.objects.get(pk=id)
        friend.delete()
        return Response({'message':'friend deleted..'},status.HTTP_201_CREATED)
    except Friend.DoesNotExist:
        return Response({'error':'user does not exist..'},status.HTTP_404_NOT_FOUND)


