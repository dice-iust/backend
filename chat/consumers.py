import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.travel_name = self.scope["url_route"]["kwargs"]["travel_name"]
        self.room_group_name = f"travel_{self.travel_name}"

        headers = dict(self.scope.get("headers", []))
        auth_header = headers.get(b"Authorization", None)
        if not auth_header:
            await self.close()
            return

        token = auth_header.decode("utf-8").split(" ")[-1] 
        user = await self.get_user_from_token(token)

        if not user:
            await self.close()
            return


        travel, travellers_group = await self.get_travel_and_group(
            self.travel_name, user
        )
        if not travel or not travellers_group:
            await self.close()
            return

        self.user = user
        self.travellers_group = travellers_group

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.save_message(message)


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
    def save_message(self, message):

        from Travels.models import ChatMessage

        ChatMessage.objects.create(
            sender=self.user,
            travellers_group=self.travellers_group,
            message=message,
            travel_name=self.travel_name,
        )

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return settings.AUTH_USER_MODEL.objects.filter(user_id=user_id).first()
        except ExpiredSignatureError:
            return None 
        except InvalidTokenError:
            return None 

    @database_sync_to_async
    def get_travel_and_group(self, travel_name, user):
        from Travels.models import Travel, TravellersGroup

        try:
            travel = Travel.objects.get(name=travel_name)
            travellers_group = TravellersGroup.objects.get(travel_is=travel)
            if user in travellers_group.users.all():
                return travel, travellers_group
            return None, None
        except (Travel.DoesNotExist, TravellersGroup.DoesNotExist):
            return None, None
