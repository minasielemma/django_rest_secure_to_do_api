import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.token = self.scope['query_string'].decode().split('=')[1]
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{user_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        try:
            access_token = AccessToken(self.token)
            self.user = await get_user(access_token['user_id'])
            await self.accept()
        except Exception as e:
            print(str(e))
            await self.close()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify_user(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
        
    async def receive(self, text_data):
        pass