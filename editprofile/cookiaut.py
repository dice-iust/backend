from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

class CookieTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):

        token = request.COOKIES.get("access_token")
        if not token:
            return None  

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

    
        user_model = get_user_model()
        try:
            user = user_model.objects.get(user_id=payload["user_id"])
        except user_model.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, None) 
