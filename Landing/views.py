from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
@api_view(['GET'])
@permission_classes([AllowAny,])
def landing_page(request):
    content={
        'text':'Start Your ADVENTURE Today!',
        'login_button':'Login',
        'signup_button':'SignUP',
        'paginate':"Let's Go ",
        'home':'Home',
        'image_url':'',
    }
    return Response(content)