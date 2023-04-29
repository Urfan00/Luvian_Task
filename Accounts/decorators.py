from django.shortcuts import redirect
from django.contrib.auth import get_user_model


User = get_user_model()


def not_authorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
