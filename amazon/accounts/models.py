
from django.db import models
from django.conf import settings
from .validators import image_size
# from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    image = models.ImageField(
        upload_to='media/images/customer', validators=[image_size], null=True, blank=True)
    birth_day = models.DateField(blank=True, null=True)
    membership = models.CharField(
        max_length=1, default=MEMBERSHIP_BRONZE, choices=MEMBERSHIP_CHOICES)
    phone = PhoneNumberField(unique=True, blank=True, null=True
                             )
    placed_at = models.DateField(auto_now=True)

    is_merchant_user = models.BooleanField(default=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Address(models.Model):
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city}, {self.street}'


class Merchant(models.Model):
    store_name = models.CharField(max_length=255, null=True, blank=True)
    cart_id = models.CharField(max_length=255, null=True, blank=True)
    card_image_front = models.ImageField(
        upload_to='midea/images/merchant/front', validators=[image_size], null=True, blank=True)
    card_image_back = models.ImageField(
        upload_to='midea/images/merchant/back', validators=[image_size], null=True, blank=True)
    is_active_in_merchant = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
