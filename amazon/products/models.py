from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from accounts.models import Customer
from .validators import image_size


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    placed_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=255)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name='products')
    merchant = models.ForeignKey(
        settings.MERCHANT_MODEL, on_delete=models.CASCADE, related_name='products', default=1)
    discount = models.FloatField(
        default=0, validators=[MinValueValidator(0)])

    class Meta:
        abstract = True


class MobileProduction(Product):
    colors = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True, null=True),
            size=8
        ),
        size=8,
        null=True,
        blank=True

    )
    model = models.CharField(max_length=255)
    ram = models.CharField(max_length=5)
    memory = models.CharField(max_length=5)
    os = models.CharField(max_length=255)
    fast_charge = models.BooleanField(default=False)


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to='media/images/products', validators=[image_size])
    product = models.ForeignKey(
        MobileProduction, on_delete=models.CASCADE, related_name='images')


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancle order')
        ]
