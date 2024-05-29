import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from api.v1.views import SaveMessageView


class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["sala"]
        self.room_group_name = "text_room_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json.get("user_id")
        username = text_data_json.get("username")
        audio = text_data_json.get("audio")

        SaveMessageView(
            userid=user_id,
            username=username,
            room=int(self.room_name),
            message=message,
            audio=audio,
        )
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message_dont_save",
                "message": message,
                "user_id": user_id,
                "username": username,
                "audio": audio,
            },
        )

    def chat_message_dont_save(self, event):
        message = event["message"]
        username = event.get("username", None)
        user_id = event.get("user_id", None)
        audio = event.get("audio", None)

        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "user_id": user_id,
                    "username": username,
                    "audio": audio,
                }
            )
        )


    def chat_message(self, event):
        message = event["message"]
        username = event.get("username", None)
        user_id = event.get("user_id", None)
        audio = event.get("audio", None)

        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "user_id": user_id,
                    "username": username,
                    "audio": audio,
                }
            )
        )
