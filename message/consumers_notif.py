import json
from os import name
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from .views import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("CONNECTED NOTIF")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.userSrc = int(self.scope['url_route']['kwargs']['srcId'])
        self.room_group_name = 'notif_%s' % self.room_name
        print(self.room_group_name,"   ",self.channel_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        

    def disconnect(self,close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("RECEIVED IN ROOM "+self.room_group_name)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        source = text_data_json['source']
        destination = text_data_json['destination']
        userSource = User.objects.get(pk=source)
        nameSource = userSource.name
        #usrId = self.userSrc
        #destId = self.userDest
        # Send message to room group
        if(destination!="none"):
            messageCon = addMessage(source,destination,message)
            time_string = messageCon.added_date.strftime("%Y/%m/%d %H:%M")
        else:
            time_string = datetime.now().strftime("%Y/%m/%d %H:%M")
        if('messageCon' in locals()):
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'idMessage':0,
                'message': message,
                'source':source,
                'destination':destination,
                'dateMessage':time_string,
                'seen':True,
                'nameSource':str(nameSource)

            }
            )

        else :
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'idMessage':0,
                    'message': message,
                    'source':source,
                    'destination':destination,
                    'dateMessage':time_string,
                    'seen':True,
                    'nameSource':str(nameSource)

                }
            )
        
        #add message to data base
    # Receive message from room group
    def chat_message(self, event):
        print("CHAAAAAT MESSAAAAGE")
        message = event['message']
        source = event['source']
        #destination=event['destination']
        dateMessage = event['dateMessage']
        """if(hasattr(event, 'nameSource')):
            print("Has nameSource")
            self.send(text_data=json.dumps({
            #'idMessage':idMessage,
            'userSrc':source,
            #'userDst':destination,
            'dateMessage':str(dateMessage),
            #'seen':seen,
            'message': message,
            'nameSource':event['nameSource']
            }))
        else:
            print("No nameSource")
            self.send(text_data=json.dumps({
            #'idMessage':idMessage,
            'userSrc':source,
            #'userDst':destination,
            'dateMessage':str(dateMessage),
            #'seen':seen,
            'message': message
            }))"""
        self.send(text_data=json.dumps({
            #'idMessage':idMessage,
            'userSrc':source,
            #'userDst':destination,
            'dateMessage':str(dateMessage),
            #'seen':seen,
            'message': message,
            'nameSource':event['nameSource']
            }))
        #seen = event['seen']
        #idMessage = event['idMessage']
        #************************************
        #userSrc = User.objects.get(pk=source).id
        #**********************************
        # Send message to WebSocket

        """self.send(text_data=json.dumps({
            #'idMessage':idMessage,
            'userSrc':source,
            #'userDst':destination,
            'dateMessage':str(dateMessage),
            #'seen':seen,
            'message': message
        }))"""
