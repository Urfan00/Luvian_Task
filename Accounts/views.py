from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .decorators import not_authorized_user


@not_authorized_user
def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def register_view(request):
    return render(request, 'register.html')


def homepage(request):
    return render(request, 'index.html')
