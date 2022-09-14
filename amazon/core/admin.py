from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email',
                    'first_name', 'last_name', 'date_joined', 'is_staff',
                    'is_superuser', 'is_active', 'customer_id']
    list_editable = ['is_staff', 'is_active']
    ordering = ['first_name', 'last_name']
    list_select_related = ['customer']
    search_fields = ['username__startswith',
                     'first_name__istartswith', 'last_name__istartswith']

    list_select_related = ['customer']

    @admin.display(ordering='customer__id')
    def customer_id(self, user):
        url = (reverse('admin:accounts_customer_changelist')
               + '?'
               + urlencode({
                   'id': user.customer.id
               }))
        return format_html(f'<a href="{url}">{user.customer.id}</a>')
