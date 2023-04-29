from django.shortcuts import render
from django.db.models import DecimalField, F, Sum, FloatField, Q
from django.db.models.functions import Cast, Coalesce
from .models import Basket, Category, Product
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required




def product_list(request):
    filter_dict = {}
    products = Product.objects.annotate(
        discount_price=Coalesce("new_price", "price", output_field=FloatField())
    ).all()
    categories = Category.objects.filter(parent__isnull=True)

    category = request.GET.get("category", None)

    if category:
        products = products.filter(
            category__in=Category.objects.get(id=int(category)).get_descendants(include_self=True)
        )
        filter_dict["category_id"]=int(category)

    min_price = request.GET.get("min_price", None)
    max_price = request.GET.get("max_price", None)

    if min_price:
        products = products.filter(discount_price__gte=min_price)
        filter_dict["min_price"] = min_price
    if max_price:
        products = products.filter(discount_price__lt=max_price)
        filter_dict["max_price"] = max_price

    query = request.GET.get('search', None)

    if query:
        products=Product.objects.filter(Q(title__icontains=query))[:6]


    paginator = Paginator(products, 8)
    page = request.GET.get("page", 1)
    product_list = paginator.get_page(page)

    context = {
        "products": product_list,
        "categories": categories,
        "filter_dict": filter_dict,
    }

    return render(request, "product-list.html", context)


@login_required(login_url='/login/')
def basket_view(request):
    products = Basket.objects.filter(user=request.user).annotate(
        discount_price = Coalesce('product__new_price', 'product__price', output_field=FloatField()),
        subtotal=F('discount_price') * F('quantity')
    )
    total_price = products.aggregate(total = Coalesce(Sum('subtotal'), 0, output_field=FloatField()))['total']
    context = {
        'products': products,
        'total_price': total_price
    }

    return render(request, 'basket.html', context)


def add_basket_view(request):
    data = {}
    product_id = request.POST.get('product_id')
    value = request.POST.get('value', None)

    product = get_object_or_404(Product, id=int(product_id))

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
    return JsonResponse(data)


def delete_basket_view(request):
    data={}
    product_id = request.POST.get('product_id')
    user_basket = Basket.objects.filter(product__id=product_id, user=request.user)
    user_basket.delete()
    products = Basket.objects.filter(user=request.user).annotate(
        discount_basket_price = Coalesce('product__new_price', 'product__price', output_field=FloatField()),
        subtotal=F('discount_basket_price')* F('quantity')
    ).annotate(
        subtotal_decimal=Cast('subtotal', output_field=DecimalField(max_digits=10, decimal_places=2))
    )
    data['total'] = products.aggregate(total = Coalesce(Sum('subtotal_decimal'), 0, output_field=DecimalField(max_digits=10, decimal_places=2)))['total']
    return JsonResponse(data)


