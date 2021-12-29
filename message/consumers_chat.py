import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from .views import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("CONNECTED CHAT")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.userSrc = int(self.scope['url_route']['kwargs']['srcId'])
        self.userDest = int(self.scope['url_route']['kwargs']['destId'])
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        list_messages = getAllMessage(self.userSrc,self.userDest)
        for msg in list_messages :
            time_string = msg.added_date.strftime("%Y/%m/%d %H:%M")
            self.send(text_data=json.dumps({
                'idMessage':msg.id,
                'userSrc':msg.userSrc.id,
                'userDst':msg.userDst.id,
                'dateMessage':time_string,
                'seen':msg.seen,
                'message':msg.content
            }))

    def disconnect(self,close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("RECEIIIIVE")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        source = text_data_json['source']
        destination = text_data_json['destination']
        usrId = self.userSrc
        destId = self.userDest
        # Send message to room group
        messageCon = addMessage(usrId,destId,message)
        time_string = messageCon.added_date.strftime("%Y/%m/%d %H:%M")
        async_to_sync(self.channel_layer.group_add)(
            "notif_room_"+destination,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            "notif_room_"+destination,
            {
                'type': 'chat_message',
                'idMessage':messageCon.id,
                'message': message+"HAHAHAHAHAHAHA",
                'source':source,
                'destination':destination,
                'dateMessage':time_string,
                'seen':messageCon.seen

            }
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'idMessage':messageCon.id,
                'message': message,
                'source':source,
                'destination':destination,
                'dateMessage':time_string,
                'seen':messageCon.seen

            }
        )
        
        #print("JOINING ROOM : "+"notif_room_"+destination)
        
        #print("Sending the message")
        """async_to_sync(self.channel_layer.group_send)(
            "notif_room_"+destination,
            {
                'type': 'chat_message',
                'idMessage':messageCon.id,
                'message': message+"HAHAHAHAHAHAHA",
                'source':source,
                'destination':destination,
                'dateMessage':time_string,
                'seen':messageCon.seen

            }
        )"""
        #add message to data base
    # Receive message from room group
    def chat_message(self, event):
        print("CHAAAAAT MESSAAAAGE")
        message = event['message']
        source = event['source']
        #destination=event['destination']
        dateMessage = event['dateMessage']
        #seen = event['seen']
        #idMessage = event['idMessage']
        #************************************
        #userSrc = User.objects.get(pk=source).id
        #**********************************
        # Send message to WebSocket
        print("THE MESSAGE WE SENT : "+message)
        self.send(text_data=json.dumps({
            #'idMessage':idMessage,
            'userSrc':source,
            #'userDst':destination,
            'dateMessage':str(dateMessage),
            #'seen':seen,
            'message': message
        }))
