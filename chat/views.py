from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatSerializer
from .models import ChatMessage, TravellersGroup
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView



class ChatMessageView(APIView):

    def get_user_from_request(self, request):
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
        return user

    def get(self, request):
        user=get_user_from_request(request)
        travel_name = request.data.get('travel_name')
        travel = get_object_or_404(Travel, name=travel_name)

        travellers_group = get_object_or_404(TravellersGroup, travel_is=travel)
        if user not in travellers_group.users.all():
            return Response(
                {"detail": "You are not part of this travel group."}, status=403
            )
        messages = ChatMessage.objects.filter(
            travellers_group=travellers_group
        ).order_by("timestamp")
        serializer = ChatSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = get_user_from_request(request)
        travel_name = request.data.get("travel_name")
        travel = get_object_or_404(Travel, name=travel_name)
        travellers_group = get_object_or_404(TravellersGroup, travel_is=travel)
        sender = user
        if sender not in travellers_group.users.all():
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
