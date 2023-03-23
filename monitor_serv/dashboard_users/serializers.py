from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from dashboard_users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        user = CustomUser(**data)
        password = data.get('password')

        try:
            validate_password(password, user)
        except ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise ValidationError(
                {'password': serializer_errors['non_field_errors']}
            )

        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=True,
        max_length=128,
        write_only=True,
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(
                password=password,
                username=username
            )

            if not user:
                msg = _("Пользователь не найден либо неправильные данные пользователя.")
                raise ValidationError(msg, code="authorization")
            if not user.is_active:
                msg = _("Пользователь не активирован.")
                raise ValidationError(msg, code="authorization")

        else:
            msg = _("Запрос должен содержать имя пользователя и пароль!")
            raise ValidationError(msg, code="authorization")

        data['user'] = user
        return data
