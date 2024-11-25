from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .serializers import UserProfileUpdateSerializer
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileUpdateSerializer
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

@method_decorator(csrf_exempt, name="dispatch")
class UserProfileUpdateAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_classes = UserProfileUpdateSerializer

    def get_serializer_class(self):
        return UserProfileUpdateSerializer

    def get(self, request):
        user_token = request.COOKIES.get("access_token")
        if not user_token:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()

        serializer = UserProfileUpdateSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user_token = request.COOKIES.get("access_token")
        if not user_token:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()

        serializer = UserProfileUpdateSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class putmethod(APIView):

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

        return user, None

    def get(self, request):
        user, error = self.authenticate_user(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserProfileUpdateSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user, error = self.authenticate_user(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserProfileUpdateSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework.authentication import TokenAuthentication
# # from .serializers import UserProfileUpdateSerializer
# # import jwt
# # from django.conf import settings
# # from django.contrib.auth import get_user_model
# # from signup.generate import generate_access_token
# # from rest_framework.generics import GenericAPIView
# # class UserProfileUpdateAPIView(GenericAPIView):
# #     authentication_classes = [TokenAuthentication]
# #     # serializer_classes = UserProfileUpdateSerializer
# #     renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
# #
# #     def get_serializer_class(self):
# #         return UserProfileUpdateSerializer
# #     def get(self, request):
# #         user_token = request.COOKIES.get("access_token")
# #         if not user_token:
# #             return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
# #         payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
# #
# #         user_model = get_user_model()
# #         user = user_model.objects.filter(user_id=payload["user_id"]).first()
# #         default_data = {
# #             "currentPassword": None,
# #             "newPassword": None,
# #             "confirmPassword": None
# #         }
# #         serializer = UserProfileUpdateSerializer(user)
# #         response_data = {**serializer.data, **default_data}
# #         return Response(response_data, status=status.HTTP_200_OK)
# #
# #     def put(self, request):
# #         user_token = request.COOKIES.get("access_token")
# #         if not user_token:
# #             return Response(
# #                 {"detail": "Authentication required"},
# #                 status=status.HTTP_401_UNAUTHORIZED,
# #             )
# #         payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
# #
# #         user_model = get_user_model()
# #         user = user_model.objects.filter(user_id=payload["user_id"]).first()
# #
# #         serializer = UserProfileUpdateSerializer(
# #             user, data=request.data, partial=True, context={"request": request}
# #         )
# #
# #         if serializer.is_valid():
# #             serializer.save()
# #             access_token = generate_access_token(user)
# #             data = {"access_token": access_token}
# #
# #             response = Response(serializer.data, status=status.HTTP_201_CREATED)
# #             response.set_cookie(key="access_token", value=access_token, httponly=True)
# #
# #             return response
# #
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
# from .serializers import UserProfileUpdateSerializer
# import jwt
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from signup.generate import generate_access_token
# from rest_framework.generics import GenericAPIView

# class UserProfileUpdateAPIView(GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

#     def get_serializer_class(self):
#         return UserProfileUpdateSerializer

#     def get(self, request):
#         user_token = request.COOKIES.get("access_token")
#         if not user_token:
#             return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
#         payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

#         user_model = get_user_model()
#         user = user_model.objects.filter(user_id=payload["user_id"]).first()

#         serializer = UserProfileUpdateSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request):
#         user_token = request.COOKIES.get("access_token")
#         if not user_token:
#             return Response(
#                 {"detail": "Authentication required"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

#         user_model = get_user_model()
#         user = user_model.objects.filter(user_id=payload["user_id"]).first()

#         serializer = UserProfileUpdateSerializer(
#             user, data=request.data, partial=True, context={"request": request}
#         )

#         if serializer.is_valid():
#             serializer.save()
#             access_token = generate_access_token(user)
#             response = Response(serializer.data, status=status.HTTP_201_CREATED)
#             response.set_cookie(key="access_token", value=access_token, httponly=True)

#             return response

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
