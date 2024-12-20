import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from asgiref.sync import sync_to_async
from ably import AblyRest
import logging
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Initialize travel and group name
            self.travel_name = self.scope["url_route"]["kwargs"]["travel_name"]
            self.room_group_name = f"travel_{self.travel_name}"

            # Initialize Ably
            self.ably = AblyRest(settings.ABLY_API_KEY)
            self.channel = self.ably.channels.get(self.room_group_name)
            logger.info(f"Connected to Ably channel: {self.room_group_name}")

            # Extract token from headers
            headers = dict(self.scope.get("headers", []))
            auth_header = headers.get(b"authorization")
            if not auth_header:
                logger.warning("Missing Authorization header.")
                await self.close(code=4003)
                return

            token = auth_header.decode("utf-8").split(" ")[-1]
            self.user = await self.get_user_from_token(token)

            # Validate user
            if not self.user:
                logger.warning("Invalid or expired token.")
                await self.close(code=4001)
                return

            # Validate travel and group
            travel, travellers_group = await self.get_travel_and_group(
                self.travel_name, self.user
            )
            if not travel or not travellers_group:
                logger.warning("Travel or travellers group not found.")
                await self.close(code=4002)
                return

            self.travellers_group = travellers_group

            # Accept the WebSocket connection
            await self.accept()

        except Exception as e:
            logger.error(f"Error in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            logger.info(
                f"{self.user.user_name} disconnected from {self.room_group_name}."
            )
        except Exception as e:
            logger.error(f"Error in disconnect: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")

            if not message:
                logger.warning("Empty message received.")
                return

            # Save the message to the database
            await self.save_message(message)

            # Publish the message to the Ably channel
            self.channel.publish(
                "chat", {"message": message, "user_name": self.user.user_name}
            )
            logger.info(f"Message published to Ably: {message}")

            # Broadcast the message to WebSocket clients
            await self.send(
                text_data=json.dumps(
                    {"message": message, "user_name": self.user.user_name}
                )
            )

        except json.JSONDecodeError:
            logger.error("Invalid JSON received.")
        except Exception as e:
            logger.error(f"Error in receive: {e}")

    @sync_to_async
    def save_message(self, message):
        from .models import ChatMessage

        if not self.user or not self.travellers_group:
            logger.warning("User or travellers group is not set.")
            return

        try:
            ChatMessage.objects.create(
                sender=self.user,
                travellers_group=self.travellers_group,
                message=message,
                travel_name=self.travel_name,
            )
            logger.info(f"Message saved to database: {message}")
        except Exception as e:
            logger.error(f"Error saving message: {e}")

    @sync_to_async
    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = get_user_model().objects.filter(user_id=user_id).first()
            logger.info(f"User retrieved: {user.user_name if user else 'None'}")
            return user
        except ExpiredSignatureError:
            logger.warning("Token has expired.")
            return None
        except InvalidTokenError:
            logger.warning("Invalid token.")
            return None
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            return None

    @sync_to_async
    def get_travel_and_group(self, travel_name, user):
        from Travels.models import Travel, TravellersGroup

        try:
            travel = Travel.objects.get(name=travel_name)
            travellers_group = TravellersGroup.objects.prefetch_related("users").get(
                travel_is=travel
            )
            if user in travellers_group.users.all() or user == travel.admin:
                logger.info(f"Travel and travellers group found for {travel_name}.")
                return travel, travellers_group
            logger.warning(
                f"User {user.user_id} is not in group for travel {travel_name}."
            )
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
