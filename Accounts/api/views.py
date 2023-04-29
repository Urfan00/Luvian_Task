from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login

User = get_user_model()


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        username = request.data['username']
        user = User.objects.get(username=username)
        login(request, user)
        request.session['username'] = username
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        token_generator = PasswordResetTokenGenerator()

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('/login/')
            # return Response({'detail': 'Account activated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Activation link is invalid or has expired'}, status=status.HTTP_400_BAD_REQUEST)
