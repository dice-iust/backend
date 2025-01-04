from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from signup.models import BlacklistedToken
import jwt
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from your_app.models import User, BlacklistedToken


@api_view(["GET"])
@permission_classes([AllowAny])
def landing_page(request):
    is_authenticated = False
    user_token = request.headers.get("Authorization")

    if user_token:
        try:

            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

            if BlacklistedToken.objects.filter(token=user_token).exists():
                raise AuthenticationFailed("Token has been blacklisted.")

            user = User.objects.filter(user_id=payload.get("user_id")).first()
            if user:
                is_authenticated = True

        except jwt.ExpiredSignatureError:
            is_authenticated = False
        except jwt.InvalidTokenError:
            is_authenticated = False
        except AuthenticationFailed:
            is_authenticated = False

    content = {
        "text": "Start Your Adventure!",
        "login_button": "Login",
        "signup_button": "Signup",
        "paginate": "Let's Go",
        "home": "Home",
        "about": "About",
        "logo_name": "Trip Tide",
        "image_url": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}landing/bluebus.png",
        "logo_image_url": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}landing/logo.png",
        "is_authenticated": is_authenticated,
    }
    return Response(content)
