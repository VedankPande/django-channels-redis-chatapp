import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from urllib import parse

from .models import Message
from django.contrib.auth import get_user_model


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        query_params = parse.parse_qs(self.scope["query_string"].decode('utf-8'))

        #create a unique room group for sender+receiver
        this_user = self.scope['url_route']['kwargs']['target']
        other_user = query_params['sender'][0]

        receive_user = get_user_model().objects.filter(pk=other_user).first()
        
        #check if other user is online
        if not receive_user.is_online():
            #self.close()
            print(f"{receive_user.username} is not online")
            
        #create a room name using the ids of the two users (sort to make sure the name is consistent)
        self.room_name = "_".join(sorted([this_user, other_user]))
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        
        query_params = parse.parse_qs(self.scope["query_string"].decode('utf-8'))
        
        #user that connected
        this_user_id = self.scope['url_route']['kwargs']['target']
        this_user = get_user_model().objects.get(pk=this_user_id)

        #user that the message is intended for
        other_user_id = query_params['sender'][0]
        other_user = get_user_model().objects.get(pk=other_user_id)
        
        #get message
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        Message.objects.create(sender=this_user, receiver=other_user, message = message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message handler for chat_message type
    def chat_message(self, event):
        
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))