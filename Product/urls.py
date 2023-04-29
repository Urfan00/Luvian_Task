from django.urls import path
from .views import add_basket_view, basket_view, delete_basket_view, product_list


urlpatterns = [
    path('product_list/', product_list, name="product_list"),
    path('add_basket/', add_basket_view, name='add_basket'),
    path('delete_basket/', delete_basket_view, name='delete_basket'),
    path('basket/', basket_view, name='basket'),
]
