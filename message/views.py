from django.shortcuts import render
from django.db.models import Q
from user.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
from rest_framework.decorators import api_view
from .models import Message
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import MessageSerializer
from user.serializers import UserSerializer
def index(request):
    return render(request, 'index.html')

def room(request, room_name,srcId,destId):
    return render(request, 'room.html', {
        'room_name': room_name,
        'srcId':srcId,
        'destId':destId
    })
def addMessage(src,dest,content):
    usrSrc = User.objects.get(pk=src)
    usrDst = User.objects.get(pk=dest)
    message = Message(userSrc=usrSrc,userDst=usrDst,content=content)
    message.save()
    return message

def deleteMessage(idMsg):
    try:
        message = Message.objects.get(pk=idMsg)
        message.delete()
    except Message.DoesNotExist :
        return Response({'error':'message does not exist !'},status=status.HTTP_404_NOT_FOUND)
def getAllMessage(request,src,dest):
    try:
        messageList = []
        messages = Message.objects.filter(Q(userSrc=src,userDst=dest) |Q(userSrc=dest,userDst=src)).order_by('added_date')
        for message in messages:
            time_string = message.added_date.strftime("%Y/%m/%d %H:%M")
            messageList.append({
                'content':message.content,
                'userSrc':message.userSrc.pk,
                'added_date':time_string
                
            })
        #serializer = MessageSerializer(messages,many=True)
        return JsonResponse(messageList,safe=False)
    except Message.DoesNotExist:
         return Response({'error':'Any message does exist !'},status=status.HTTP_404_NOT_FOUND)

@api_view(('PUT',))
@permission_classes((permissions.AllowAny,))
def seenMessage(request,id):
    try:
        message = Message.objects.get(pk=id)
        message.seen = True
        message.save()
        return Response({'error':'the message is seen'},status=status.HTTP_201_CREATED)
    except Message.DoesNotExist and AssertionError:
        return Response({'erroe':'message does not exist !'},status=status.HTTP_404_NOT_FOUND)


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def getMyConvertation(request,id):
    try:
        users = User.objects.filter(~Q(id=id))
        convertations = []
        for i in range(len(users)):
            messages = Message.objects.filter(Q(userSrc=id,userDst=users[i].id) |Q(userSrc=users[i].id,userDst=id)).order_by('added_date')
            user = UserSerializer(users[i]).data
            if(messages):
                index  = len(messages)-1
                if(len(messages[index].content)>=25):
                    message_str = messages[index].content[0:18]+"..."
                else :
                    message_str = messages[index].content
                time_string = messages[index].added_date.strftime("%H:%M")
                convertations.append({
                'user':user,
                'lastMessage':message_str,
                'time':messages[index].added_date
                })
        resultConvertations = sorted(convertations, key=lambda k: k['time'], reverse=True)
        if len(convertations)==0:
            return Response({'message':'There is no convertations...'},status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse(resultConvertations, safe=False)
    except Message.DoesNotExist :
        return Response({'error':'no message ..'},status.HTTP_404_NOT_FOUND)
    