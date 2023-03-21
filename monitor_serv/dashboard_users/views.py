from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dashboard_users.models import CustomUser
from dashboard_users.serializers import CustomUserSerializer, UserSerializer


# Create your views here.
class UserAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)


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
    authentication_classes = (IsAuthenticated,)

    def post(self, request):
        pass
