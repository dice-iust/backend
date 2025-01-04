from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProfilePageSerializer
from django.conf import settings
import jwt
from django.contrib.auth import get_user_model

from django.conf import settings
from django.contrib.auth import get_user_model
from signup.generate import generate_access_token
from rest_framework.generics import GenericAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from signup.models import BlacklistedToken

class profileView(APIView):

    def authenticate_user(self, request):

        token = request.headers.get("Authorization")
        if not token:
            return None, {"detail": "Authentication required."}

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None, {"detail": "Token has expired."}
        except jwt.InvalidTokenError:
            return None, {"detail": "Invalid token."}

        user_model = get_user_model()
        try:
            user = user_model.objects.get(user_id=payload["user_id"])
        except user_model.DoesNotExist:
            return None, {"detail": "User not found."}
        if BlacklistedToken.objects.filter(token=token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)

        return user, None

    def get(self, request):
        user, error = self.authenticate_user(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProfilePageSerializer(user, context={"request": self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
