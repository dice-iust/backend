import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from Travels.models import TravellersGroup, Travel
from rest_framework.exceptions import AuthenticationFailed


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.travel_name = self.scope["url_route"]["kwargs"]["travel_name"]
        self.room_group_name = f"travel_{self.travel_name}"

        user_token = self.scope.get("headers", {}).get("authorization", b"").decode()
        if not user_token:
            await self.close()
            return
        user = await self.get_user_from_token(user_token)
        if not user or not await self.is_user_in_travel_group(self.travel_name, user):
            await self.close()
            return
        self.user = user  
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user_name": self.user.user_name, 
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        user_name = event["user_name"]

        await self.send(
            text_data=json.dumps({"message": message, "user_name": user_name})
        )

    @database_sync_to_async
    def get_user_from_token(self, token):
        """
        Get the user from the provided JWT token.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = User.objects.filter(user_id=user_id).first()
            return user
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

    @database_sync_to_async
    def is_user_in_travel_group(self, travel_name, user):
        try:
            travel = Travel.objects.get(id=travel_name)
            travel_group = TravellersGroup.objects.get(travel_is=travel)
            return user in travel_group.users.all()
        except Travel.DoesNotExist or TravellersGroup.DoesNotExist:
            return False
