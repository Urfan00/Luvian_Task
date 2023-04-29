from rest_framework.views import APIView
from .serializers import BasketSerializer
from Product.models import Basket, Product
from rest_framework.response import Response
from rest_framework import status
from django.db.models import DecimalField, F, Sum, FloatField
from django.db.models.functions import Cast, Coalesce


class BasketAPI(APIView):
    serializer_class = BasketSerializer
    http_method_names = ['get', 'post', 'delete']

    def get(self, request, *args, **kwargs):
        basket = Basket.objects.filter(user = request.user).all()
        serializer = self.serializer_class(basket, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        value = request.data.get('value', None)

        product = Product.objects.filter(id=product_id).first()

        data = {}

        if product:
            basket_obj, created = Basket.objects.annotate(
                discount_basket_price = Coalesce('product__new_price', 'product__price', output_field=FloatField()),
            ).get_or_create(
                product=product, user=request.user, defaults={'quantity': 1}
            )

            if not value:
                if not created:
                    basket_obj.quantity += 1
                    basket_obj.save()
            else:
                basket_obj.quantity = int(value)
                basket_obj.save()

                if basket_obj.product.in_sale:
                    data['subtotal'] = basket_obj.quantity * basket_obj.product.new_price
                else:
                    data['subtotal'] = basket_obj.quantity * basket_obj.product.price

                products = Basket.objects.filter(user=request.user).annotate(
                    discount_basket_price = Coalesce('product__new_price', 'product__price', output_field=FloatField()),
                    subtotal=F('discount_basket_price')* F('quantity')
                ).annotate(
                    subtotal_decimal=Cast('subtotal', output_field=DecimalField(max_digits=10, decimal_places=2))
                )
                data['total'] = products.aggregate(total = Coalesce(Sum('subtotal_decimal'), 0, output_field=DecimalField(max_digits=10, decimal_places=2)))['total']
            return Response(data, status = status.HTTP_201_CREATED)
        return Response()
