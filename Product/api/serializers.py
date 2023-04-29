from rest_framework import serializers
from Product.models import Basket



class BasketSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Basket
        fields = ['id', 'user', 'product', 'quantity']