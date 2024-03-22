import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from api.models import Message, Usuario, Sala
from api.v1.views import SaveMessageView
from firebase_admin import storage
import base64
import tempfile

class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['sala']
        self.room_group_name = 'text_room_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json.get('user_id')
        username = text_data_json.get('username')
        print(text_data)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'username': username,
                'audio': text_data_json.get('audio')
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event.get('username', None)  
        user_id = event.get('user_id', None)  
        audio = event.get('audio', None)

        if audio is not None:
            audio_data = None
            with open(audio, 'rb') as file:
                audio_data = file.read()
            result = SaveMessageView(userid=user_id, username=username, room=int(self.room_name), message=message, audio=audio_data)
            self.send(text_data=json.dumps({
            'message': '',
            'user_id': user_id,
            'username': username,
            'audio': result
            }))
            return 
        else:
            result = SaveMessageView(userid=user_id,username=username, room=int(self.room_name), message=message, audio=None)

            self.send(text_data=json.dumps({
                'message': message,
                'user_id': user_id,
                'username': username
            }))