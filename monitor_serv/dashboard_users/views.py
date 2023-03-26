from django.contrib.auth import login, logout, authenticate
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from dashboard_users.mixins import UserSessionMixin
from dashboard_users.models import CustomUser
from dashboard_users.serializers import CustomUserSerializer, CustomUserSerializer, LoginUserSerializer, \
    CreateUserSerializer, UpdateUserSerializer

csrf_protect_method = method_decorator(csrf_protect, name="dispatch")


# Create your views here.
class UsersView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)


# @method_decorator(csrf_protect, name="dispatch")
@csrf_protect_method
class CheckAuthentication(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = self.request.user

        is_auth = user.is_authenticated

        if is_auth:
            return Response({"isAuthenticated": "success"})
        return Response({"isAuthenticated": "error"})


# @method_decorator(csrf_protect, name="dispatch")
@csrf_protect_method
class RegisterView(APIView):
    def post(self, request):
        data = request.data

        serializer = CreateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = CustomUserSerializer(user)
        return Response(user.data, status.HTTP_201_CREATED)


# @method_decorator(csrf_protect, name="dispatch")
@csrf_protect_method
class LoginUserView(APIView):
    def post(self, request):
        data = self.request.data

        serializer = LoginUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        login(request, user)

        return Response({"status": "success"}, status=status.HTTP_200_OK)


# @method_decorator(csrf_protect, name="dispatch")
@csrf_protect_method
class LogoutView(UserSessionMixin, APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # user_id = self.get_user_id_from_session(request)
        # request['user'] = CustomUser.objects.get(id=user_id)
        logout(request)
        return Response({"success": "logout"})


class UpdateUserView(UserSessionMixin, APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        # user_id = self.get_user_id_from_session(request)
        user = self.request.user
        data = self.request.data

        serializer = UpdateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user.id)
            serializer.update(user, data)
            return Response({"success": "user is updated"}, status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "user is not found"}, status.HTTP_400_BAD_REQUEST)


@csrf_protect_method
class DeleteUserView(UserSessionMixin, APIView):
    authentication_classes = (IsAuthenticated,)

    def delete(self, request):
        # user_id = self.get_user_id_from_session(request)
        user = self.request.user

        try:
            user = CustomUser.objects.get(id=user.id)
            user.delete()
            return Response({"success": "user is deleted."})
        except CustomUser.DoesNotExist:
            return Response({"error": "user is not found"})


class RetrieveUserView(UserSessionMixin, APIView):
    def get(self, request):
        user_id = self.get_user_id_from_session(request)

        user = CustomUser.objects.get(id=user_id)

        if user.is_anonymous:
            return Response({"error": "anonymous user"}, status.HTTP_400_BAD_REQUEST)

        user = CustomUserSerializer(user)

        return Response(user.data, status=status.HTTP_200_OK)
