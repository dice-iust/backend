import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import logging

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.travel_name = self.scope["url_route"]["kwargs"]["travel_name"]
            self.room_group_name = f"travel_{self.travel_name}"

            query_string = self.scope.get("query_string", b"").decode("utf-8")
            token = None

            if query_string:
                query_params = dict(qc.split("=") for qc in query_string.split("&"))
                token = query_params.get("token")

            if not token:
                logger.warning("Missing token in query parameters.")
                await self.close(code=4003)
                return
            user = await self.get_user_from_token(token)

            if not user:
                logger.warning("Invalid or expired token.")
                await self.close(code=4001)
                return

            travel, travellers_group = await self.get_travel_and_group(
                self.travel_name, user
            )
            if not travel or not travellers_group:
                logger.warning("Travel or travellers group not found.")
                await self.close(code=4002)
                return

            self.user = user
            self.travellers_group = travellers_group

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            last_messages = await self.get_all_messages()
            await self.send(text_data=json.dumps({"last_messages": last_messages}))

        except Exception as e:
            logger.error(f"Error in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            if self.channel_layer:
                await self.channel_layer.group_discard(
                    self.room_group_name, self.channel_name
                )
            else:
                logger.warning("Channel layer is not available during disconnect.")
        except Exception as e:
            logger.error(f"Error in disconnect: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")

            if not message:
                logger.warning("Empty message received.")
                return

            saved_message = await self.save_message(message)

            if not saved_message:
                logger.error("Failed to save message.")
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    **saved_message,
                },
            )
        except json.JSONDecodeError:
            logger.error("Invalid JSON received.")
        except Exception as e:
            logger.error(f"Error in receive: {e}")

    async def chat_message(self, event):
        try:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": event["message"],
                        "user_name": event["user_name"],
                        "profile": event["profile"],
                        "time": event["time"],
                    }
                )
            )
        except Exception as e:
            logger.error(f"Error in chat_message: {e}")

    @database_sync_to_async
    def save_message(self, message):
        from .models import ChatMessage
        from pytz import timezone as pytz_timezone

        if not self.user or not self.travellers_group:
            logger.warning("User or travellers group is not set.")
            return None

        try:
            # Use the Iran timezone for the timestamp
            iran_timezone = pytz_timezone("Asia/Tehran")

            # Save the message with the current timestamp
            chat_message = ChatMessage.objects.create(
                sender=self.user,
                travellers_group=self.travellers_group,
                message=message,
                travel_name=self.travel_name
            )

            # Construct the profile URL
            profile_url = (
                f"https://triptide.liara.run{self.user.profilePicture.url}"
                if self.user.profilePicture
                else None
            )

            # Convert timestamp to Iran timezone
            timestamp = chat_message.timestamp.astimezone(iran_timezone).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            return {
                "message": chat_message.message,
                "user_name": self.user.user_name,
                "profile": profile_url,
                "time": timestamp,
            }

        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return None


    @database_sync_to_async
    def get_travel_and_group(self, travel_name, user):
        from Travels.models import Travel, TravellersGroup

        try:
            travel = Travel.objects.get(name=travel_name)
            travellers_group = TravellersGroup.objects.prefetch_related("users").get(
                travel_is=travel
            )
            if user in travellers_group.users.all() or user == travel.admin:
                return travel, travellers_group
            logger.warning(f"User {user.id} is not in group for travel {travel_name}.")
            return None, None
        except Travel.DoesNotExist:
            logger.warning(f"Travel {travel_name} does not exist.")
            return None, None
        except TravellersGroup.DoesNotExist:
            logger.warning(f"Travellers group for travel {travel_name} does not exist.")
            return None, None
        except Exception as e:
            logger.error(f"Error in get_travel_and_group: {e}")
            return None, None

        
    @database_sync_to_async
    def get_all_messages(self):
        from .models import ChatMessage
        from pytz import timezone as pytz_timezone

        try:
            messages = ChatMessage.objects.filter(
                travellers_group=self.travellers_group, travel_name=self.travel_name
            ).order_by("timestamp")

            # Use the Iran timezone for all message timestamps
            iran_timezone = pytz_timezone("Asia/Tehran")

            return [
                {
                    "user_name": msg.sender.user_name,
                    "message": msg.message,
                    "profile": (
                        f"https://triptide.liara.run{msg.sender.profilePicture.url}"
                        if msg.sender.profilePicture
                        else None
                    ),
                    "time": msg.timestamp.astimezone(iran_timezone).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                for msg in messages
            ]
        except Exception as e:
            logger.error(f"Error retrieving all messages: {e}")
            return []
