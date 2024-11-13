from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny,])
def landing_page(request):
    content = {
        "text": "Start Your ADVENTURE Today !",
        "login_button": "Log In",
        "signup_button": "Sign UP",
        "paginate": "Let's Go ",
        "home": "Home",
        "about": "About",
        "logo_name": "Trip Tide",
        "image_url": f"{settings.MEDIA_URL}landing/bus.jpg",
        "logo_image_url": f"{settings.MEDIA_URL}landing/logo.jpg",
    }
    return Response(content)
