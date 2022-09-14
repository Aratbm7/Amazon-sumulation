
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode

from .models import Address, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'membership',
                    'merchant', 'phone', 'birth_day', 'customer_address', 'user_info', 'image']
    list_editable = ['membership', 'merchant']
    list_select_related = ['user', 'address']
    ordering = ['id']

    def full_name(self, customer):
        return f'{customer.user.first_name} {customer.user.last_name}'

    @admin.display(ordering='address__city')
    def customer_address(self, customer):
        url = (reverse('admin:accounts_address_changelist')
               + '?'
               + urlencode({
                   'customer__id': customer.id
               }))
        return format_html(f'<a href="{url}">{customer.address.city}</a>')

    @admin.display(ordering='user__date_joined')
    def user_info(self, customer):
        url = (reverse('admin:core_user_changelist')
               + '?'
               + urlencode({
                   'id': customer.user_id
               }))

        return format_html(f'<a href="{url}">{customer.user.username}</a>')

# Register your models here.


@ admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'street', 'code', 'customer_username']
    ordering = ['city']
    list_select_related = ['customer', 'customer__user']

    def customer_username(self, address):
        url = (reverse('admin:accounts_customer_changelist')
               + '?'
               + urlencode({
                   'id': address.customer_id
               }))

        return format_html(f'<a href="{url}">{address.customer.user.username}</a>')
