from django.urls import path
from .views import homepage, login_view, logout_view, register_view


urlpatterns = [
    path('login/', login_view, name='login_page'),
    path('register/', register_view, name='register_page'),
    path('logout/', logout_view, name = 'logout'),
    path('', homepage, name='index')
]
