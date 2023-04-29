from django.shortcuts import reverse
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from services.generator import Generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from Accounts.tasks import send_activation_email
from rest_framework import status


User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                {"error": "username or password is wrong"}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"error": "Your account is not active"}
            )

        return attrs

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        user = User.objects.get(username=instance.get("username"))
        token = RefreshToken.for_user(user)
        repr_["tokens"] = {"refresh": str(token),"access": str(token.access_token)}
        return repr_


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "slug", "password", "password_confirm")
        extra_kwargs = {
            "password": {"write_only": True},
            "slug": {"read_only": True},
        }

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get("email")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")


        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"error": "This username already exists"}
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"error": "This email already exists"}
            )

        if len(password) < 8:
            raise serializers.ValidationError(
                {"error": "Password must be at least 8 characters"}
            )

        if password != password_confirm:
            raise serializers.ValidationError(
                {"error": "Password and Confirm password don't match"}
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        user = User.objects.create(
            **validated_data, is_active=False
        )
        user.set_password(password)
        user.save()

        # Generate activation link and send activation email
        uid = urlsafe_base64_encode(force_bytes(user.id))

        token = PasswordResetTokenGenerator().make_token(user)

        activation_link = self.context['request'].build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uid, 'token': token})
        )

        send_activation_email.delay(user.email, activation_link)

        return user
