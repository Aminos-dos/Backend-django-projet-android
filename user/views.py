from functools import cache
from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from .serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
from .models import User
from rest_framework.response import Response
import random
from django.core.mail import EmailMessage
from friend.models import Friend
from django.db.models import Q
from request.models import Request
import PIL.Image as Image
import io
import base64
import os
from pathlib import Path
from django.core.files import File 
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        photoExist = False
        if 'photo' in data:
            b=base64.b64decode(data['photo'])
            img=Image.open(io.BytesIO(b))
            image_path ="/home/aminos/Documents/Projet Android/Api/AndroidApi/images/"+data['username']
            path = Path(image_path)
            path.mkdir(parents=True, exist_ok=True)
            img.save(f"{image_path}/image_profile.png")
            del data['photo']
            photoExist=True
        serializer = UserSerializer(data=data)
        passwd = data['password']
        data['password'] = make_password(passwd)
        if serializer.is_valid():
            serializer.save()
            if photoExist:
                user = User.objects.get(username=data['username'])
                user.photo = 'images/'+data['username']+'/image_profile.png'
                user.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors,status=400)
@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def signin(request):
    data = JSONParser().parse(request)
    try:
        print("Request est : "+str(data))
        user = User.objects.get(username=data['username'])
        if(check_password(data['password'],user.password)):
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data,safe=False)
        else :
            return Response({'error':'wrong password ..'},status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist :
        return Response({'error':'mail or password is wrong ..'},status.HTTP_404_NOT_FOUND)
@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def getAllUsers(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return JsonResponse(serializer.data,safe=False)
    except User.DoesNotExist :
        return Response({'error':'no users ..'},status.HTTP_404_NOT_FOUND)
@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def searchUserByName(request,name):
    try:
        users = User.objects.filter(name__iregex=r'^.*'+name+'.*$')
        serializer = UserSerializer(users,many=True)
        return JsonResponse(serializer.data,safe=False)
    except User.DoesNotExist :
        return Response({'error':'no users ..'},status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(('PUT',))
@permission_classes((permissions.AllowAny,))
def updateUser(request,id):
    user = User.objects.get(pk=id)
    user_data = JSONParser().parse(request) 
    photoExist = False
    if 'photo' in user_data:
        b=base64.b64decode(user_data['photo'])
        img=Image.open(io.BytesIO(b))
        image_path ="/home/aminos/Documents/Projet Android/Api/AndroidApi/images/"+user_data['username']
        path = Path(image_path)
        path.mkdir(parents=True, exist_ok=True)
        img.save(f"{image_path}/image_profile.png")
        del user_data['photo']
        photoExist=True
    if not user_data['password']:
        user_data['password'] = user.password
    else:
        user_data['password'] = make_password(user_data['password'])
    user_serializer = UserSerializer(user, data=user_data) 
    if user_serializer.is_valid(): 
        user_serializer.save() 
        if photoExist:
            user = User.objects.get(username=user_data['username'])
            user.photo = 'images/'+user_data['username']+'/image_profile.png'
            user.save()
        return JsonResponse(user_serializer.data) 
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(('PUT',))
@permission_classes((permissions.AllowAny,))

def resetPassword(request):
    data = JSONParser().parse(request) 
    try:
        print('Request is : '+str(data))
        user = User.objects.get(email=data['email'])
        new_password = str(random.randint(1000,99999999))
        email = EmailMessage(subject="Reset Password",body="Bonjour "+user.name+" le nouveau mot de passe : "+str(new_password)+ " svp changer ce mot de passe",to=[data['email']])
        email.send()
        user.password = make_password(new_password)
        user.save()
        return Response({'messsage':'Check your email for reset your password..'},status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error':'no user exists with this email ..'},status=status.HTTP_404_NOT_FOUND)


@api_view(('DELETE',))
@permission_classes((permissions.AllowAny,))

def deleteUser(request,id):
    try:
        user = User.objects.get(pk=id)
        user.delete()
        return Response({'messsage':'user deleted..'},status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'message':'user does not exist ...'},status=status.HTTP_404_NOT_FOUND)

def isFriend(id1,id2):
    try:
        friend  = Friend.objects.get(Q(friend1=id1,friend2=id2)|(Q(friend1=id2,friend2=id1)))
        if friend :
            return True
        else:
            return False
    except Friend.DoesNotExist:
        return False
def isRequestSend(id1,id2):
    try:
        request = Request.objects.get(sender=id1,receiver=id2)
        if (request):
            return True
        else :
            return False
    except Request.DoesNotExist:
        return False 
def isReciveRequest(id1,id2):
    try:
        request = Request.objects.get(sender=id2,receiver=id1)
        if (request):
            return True
        else :
            return False
    except Request.DoesNotExist:
        return False 
@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def getUsers(request,id):
    try:
        users = User.objects.filter(~Q(pk=id))
        users_all = []
        for i in range(len(users)):
            user= UserSerializer(users[i]).data
            status=""
            if(isFriend(id,users[i].id)):
                status="Ami"
            elif (isRequestSend(id,users[i].id)):
                status="Invitation envoyée"
            elif(isReciveRequest(id,users[i].id)):
                status="Accepter"
            else:
                status="Inviter"
            users_all.append({
            'user':user,
            'status':status,
            })
        users_all_sorted = sorted(users_all, key=lambda k: k['status'], reverse=False)
        return JsonResponse(users_all_sorted,safe=False)
    except User.DoesNotExist :
        return Response({'error':'no users ..'},status.HTTP_404_NOT_FOUND)