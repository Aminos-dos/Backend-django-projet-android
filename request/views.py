from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from .serializers import RequestSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
from .models import Request
from rest_framework.response import Response
from .serializers import RequestSerializer
from friend.models import Friend

@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def sendRequest(request):
    data = JSONParser().parse(request)
    serializer = RequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)
@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def acceptRequest(request):
    data = JSONParser().parse(request)
    req = Request.objects.get(sender=data['sender'],receiver=data['receiver'])
    req.delete()
    friend = Friend(friend1=req.sender,friend2=req.receiver)
    friend.save()
    return Response({'message':'Request accepted..'},status.HTTP_201_CREATED)
    
@api_view(('DELETE',))
@permission_classes((permissions.AllowAny,))
def deleteRequest(request,id):
    request = Request.objects.get(pk=id)
    request.delete()
    return Response({'message':'Request is deleted..'},status.HTTP_201_CREATED)
