from django.contrib import admin
from .models import Basket, Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'p_image', 'title', 'category', 'price', 'in_sale', 'discount', 'new_price']
    search_fields = ['title']
    list_filter = ['in_sale']

class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'quantity']


admin.site.register(Basket, BasketAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
