from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dashboard_users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'date_joined')


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        max_length=255, label="Confirm password", write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.pop('password2')

        try:
            if password != password_confirmation:
                raise ValidationError('passwords are not match')

            validate_password(password, user=CustomUser(**data))
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
            is_active=False
        )

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


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
            elif not user.is_active:
                msg = _("Пользователь не активирован.")
                raise ValidationError(msg, code="authorization")

        else:
            msg = _("Запрос должен содержать имя пользователя и пароль!")
            raise ValidationError(msg, code="authorization")

        data['user'] = user
        return data
