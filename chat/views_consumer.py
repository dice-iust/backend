from ably import AblyRest
from django.conf import settings
import logging
from rest_framework.response import Response
from adrf.decorators import api_view
from rest_framework import status
from .models import ChatMessage
from Travels.models import Travel, TravellersGroup
import jwt
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

@api_view(["POST"])
async def AblyMessagePublishView(request):
    message = request.data.get("message")
    travel_name = request.data.get("travel_name")
    token = request.headers.get("Authorization")
    if not message or not travel_name or not token:
        return Response(
            {"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = await get_user_from_token(token)
    if not user:
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST
        )

    travel, tg = await get_travel_and_group(travel_name, user)
    if not travel or not tg:
        return Response(
            {"error": "Travel or group not found or unauthorized"},
            status=status.HTTP_403_FORBIDDEN,
        )

    ably = AblyRest("w9hDjQ.bDJwDg:nV7gxEThhWT4clJqHv9K3syB3SQCDrkcgaoChiWmRQY")
    room_group_name = f"travel_{travel_name}"
    channel = ably.channels.get(room_group_name)

    await channel.publish("chat", {"message": message, "user_name": user.user_name})

    await sync_to_async(ChatMessage.objects.create)(
        sender=user,
        travellers_group=tg,
        message=message,
        travel_name=travel_name,
    )

    logger.info(f"Message published to Ably channel: travel_{travel_name}")
    return Response(
        {"status": "Message published successfully"}, status=status.HTTP_200_OK
    )

async def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        user = await get_user_model().objects.filter(user_id=user_id).afirst()
        return user
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
    return None

async def get_travel_and_group(travel_name, user):
    try:
        travel = await Travel.objects.aget(name=travel_name)
        travellers_group = await TravellersGroup.objects.prefetch_related("users").aget(
            travel_is=travel
        )
        if user in travellers_group.users.all() or user == travel.admin:
            logger.info(f"Travel and travellers group found for {travel_name}.")
            return travel, travellers_group
        logger.warning(f"User {user.user_id} is not in group for travel {travel_name}.")
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
