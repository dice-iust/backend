from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatSerializer,GetProfileSerializer
from .models import ChatMessage
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from Travels.models import Travel, TravellersGroup
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status

class ChatMessageView(APIView):

    def get(self, request):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        travel_name = request.data.get('travel_name')
        travel = get_object_or_404(Travel, name=travel_name)

        travellers_group = get_object_or_404(TravellersGroup, travel_is=travel)
        if user not in travellers_group.users.all() and user!=travel.admin:
            return Response(
                {"detail": "You are not part of this travel group."}, status=403
            )
        messages = ChatMessage.objects.filter(
            travellers_group=travellers_group
        ).order_by("timestamp")
        serializer = ChatSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        travel_name = request.data.get("travel_name")
        travel = get_object_or_404(Travel, name=travel_name)
        travellers_group = get_object_or_404(TravellersGroup, travel_is=travel)
        sender = user
        if sender not in travellers_group.users.all()and sender !=travel.admin:
            return Response(
                {"detail": "You are not part of this travel group."}, status=403
            )

        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(travellers_group=travellers_group,sender=sender,travel_name=travel_name)
            return Response(
                serializer.data, status=201
            ) 
        return Response(serializer.errors, status=400)


class profileView(APIView):
    def get(self,request):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        user_name_show = request.query_params.get("user_name")
        user_show = user_model.objects.filter(user_name=user_name_show).first()
        if not user_show:
            return Response("this user is not exit.",status=status.HTTP_404_NOT_FOUND)
        serializer=GetProfileSerializer(user_show, context={"request": self.request}).data
        return Response(serializer,status=status.HTTP_200_OK)
        return Response("some error",status=status.HTTP_400_BAD_REQUEST)
