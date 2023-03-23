from django.contrib.auth import login
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from dashboard_users.models import CustomUser
from dashboard_users.serializers import CustomUserSerializer, UserSerializer, LoginUserSerializer

csrf_protect_method = method_decorator(csrf_protect)


# Create your views here.
class UserAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)
        return Response(user.data, status.HTTP_201_CREATED)


class RetrieveUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_200_OK)


class LoginUserAPIView(APIView):
    @csrf_protect_method
    def post(self, request):
        serializer = LoginUserSerializer(request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        login(request, user)

        return Response({"status": "success"}, status=status.HTTP_200_OK)

