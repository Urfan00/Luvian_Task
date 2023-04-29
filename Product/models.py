from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from decimal import Decimal

User = get_user_model()


class Category(MPTTModel, models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    discounts = (
        (5, '5'),
        (10, '10'),
        (15, '15'),
        (20, '20'),
        (25, '25'),
        (30, '30'),
        (35, '35'),
        (40, '40'),
        (45, '45'),
        (50, '50'),
        (55, '55'),
        (60, '60'),
        (65, '65'),
        (70, '70'),
        (75, '75'),
        (80, '80'),
        (85, '85'),
        (90, '90'),
        (95, '95'),
        (100, '100')
    )
    title = models.CharField(max_length=50)
    p_image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_sale = models.BooleanField(default=False)
    discount = models.IntegerField(choices=discounts, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.in_sale:
            discount_decimal = Decimal(self.discount) / 100
            self.new_price = self.price - self.price * discount_decimal
        return super().save(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} ==> {self.product.title}"
