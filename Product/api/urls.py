from django.urls import path
from .views import BasketAPI

urlpatterns = [
    path('basket/', BasketAPI.as_view(), name='baskets')
]
