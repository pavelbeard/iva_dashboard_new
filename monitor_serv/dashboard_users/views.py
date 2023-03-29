from http import HTTPStatus

from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard_users.mixins import UserSessionMixin
from dashboard_users.models import CustomUser
from dashboard_users.serializers import CustomUserSerializer, LoginUserSerializer, \
    CreateUserSerializer, UpdateUserSerializer

csrf_protect_method = method_decorator(csrf_protect, name="dispatch")


# Create your views here.
class UsersView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CheckAuthentication(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        user = self.request.user

        try:
            user = CustomUser.objects.get(id=user.id)
            if user.is_authenticated:
                return Response({"isAuthenticated": "success"}, status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"isAuthenticated": "error"}, HTTPStatus.UNAUTHORIZED)


# @method_decorator(csrf_protect, name="dispatch")
@csrf_protect_method
class RegisterView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = self.request.data

        serializer = CreateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = CustomUserSerializer(user)
        return Response({"success": "user created", "userData": user.data}, status.HTTP_201_CREATED)


@csrf_protect_method
class LoginUserView(APIView):
    permission_classes = (AllowAny, )

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
class LogoutView(APIView):
    def post(self, request):
        logout(self.request)
        return Response({"success": "you are logout"}, status.HTTP_200_OK)


@csrf_protect_method
class UpdateUserView(APIView):
    def put(self, request):
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
class DeleteUserView(APIView):
    def delete(self, request):
        user = self.request.user

        try:
            user = CustomUser.objects.get(id=user.id)
            user.delete()
            return Response({"success": "user is deleted"}, status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "user is not found"}, status.HTTP_400_BAD_REQUEST)


@csrf_protect_method
class RetrieveUserView(APIView):
    def get(self, request):
        user = self.request.user

        try:
            user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return Response({"error": "user is not found or anonymous"}, status.HTTP_400_BAD_REQUEST)

        user = CustomUserSerializer(user)
        user_data = user.data
        del user_data['password']

        return Response(user_data, status=status.HTTP_200_OK)
