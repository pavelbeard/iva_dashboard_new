from http import HTTPStatus

from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard_users.models import CustomUser
from dashboard_users.serializers import CustomUserSerializer, LoginUserSerializer, \
    CreateUserSerializer, UpdateUserSerializer

csrf_protect_method = method_decorator(csrf_protect, name="dispatch")


# Create your views here.
class UsersView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CheckAuthentication(APIView):
    def get(self, request):
        return Response({"isAuthenticated": "true"})
        #
        # user = self.request.user
        #
        # try:
        #     user = CustomUser.objects.get()
        #     if user.is_authenticated:
        #         return Response({"isAuthenticated": "success"}, status.HTTP_200_OK)
        # except CustomUser.DoesNotExist:
        #     return Response({"isAuthenticated": "error"}, HTTPStatus.UNAUTHORIZED)


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
        msg = _("Вы успешно зарегистрированы, дождитесь активации учетной записи администратором.")
        return Response({"success": msg, "userData": user.data}, status.HTTP_201_CREATED)


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
        return Response({"success": user.username}, status=status.HTTP_200_OK)


@csrf_protect_method
class LogoutView(APIView):
    def post(self, request):
        logout(self.request)
        msg = _("Удачного мониторинга без дашборда 🤣")
        return Response({"success": msg}, status.HTTP_200_OK)


@csrf_protect_method
class UpdateUserView(APIView):
    def put(self, request):
        user = self.request.user
        data = self.request.data

        serializer = UpdateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get()
            serializer.update(user, data)
            return Response({"success": "user is updated"}, status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "user is not found"}, status.HTTP_400_BAD_REQUEST)


@csrf_protect_method
class DeleteUserView(APIView):
    def delete(self, request):
        user = self.request.user

        try:
            user = CustomUser.objects.get()
            user.delete()
            msg = _("пользователь удален")
            return Response({"success": msg}, status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            msg = _("user is not found")
            return Response({"error": msg}, status.HTTP_400_BAD_REQUEST)


class RetrieveUserView(APIView):
    def get(self, request):
        user = self.request.user

        try:
            user = CustomUser.objects.get()
        except CustomUser.DoesNotExist:
            msg = _("anonymous")
            return Response({"error": msg}, status.HTTP_400_BAD_REQUEST)

        user = CustomUserSerializer(user)
        user_data = user.data
        del user_data['password']
        return Response(user_data, status=status.HTTP_200_OK)
