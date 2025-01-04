from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from signup.models import BlacklistedToken

@api_view(['GET'])
@permission_classes([AllowAny,])
def landing_page(request):
    is_authenticated = False
    user_token = request.headers.get("Authorization")
    if not user_token:            
        is_authenticated = False
    try:
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:            
        is_authenticated = False
    except jwt.InvalidTokenError:            
        is_authenticated = False
    user = User.objects.filter(user_id=payload["user_id"]).first()        
    if user:
        is_authenticated = True
    if BlacklistedToken.objects.filter(token=user_token).exists():
        is_authenticated = False
    content = {
        "text": "Start Your Adventure !",
        # "text3": "ADVENTURE",
        # "text4": "Today !",
        "login_button": "Login",
        "signup_button": "Signup",
        "paginate": "Let's Go ",
        "home": "Home",
        "about": "About",
        "logo_name": "Trip Tide",
        "image_url": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}landing/bluebus.png",
        "logo_image_url": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}landing/logo.png",
        'is_authenticated':is_authenticated
    }
    return Response(content)
