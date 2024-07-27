import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route'] ['kwargs'] ['room_name']
        self.room_group_name = self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def receive(self, text_data):
        json_text = json.loads(text_data)
        message = json_text.get("message")
        from_user = json_text.get("from_user")
        print(json_text, "=-=-=-==-=-=-=-=")
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message,
                "from_user": from_user,
            }
        )
    
    def chat_message(self, event):
        message = event.get('message')
        from_user = event.get("from_user")
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "from_user": from_user}))