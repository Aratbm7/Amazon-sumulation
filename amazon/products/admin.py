from django.contrib import admin

from accounts.models import Merchant
from .models import MobileProduction


@admin.register(MobileProduction)
class MobileProductionAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'slug', 'merchant')
    list_select_related = ['merchant']
    prepopulated_fields = {'slug': ('title',)}

    def get_exclude(self, request, obj):
        if request.user.is_superuser or (request.user.is_staff and not request.user.is_merchant):
            return super(MobileProductionAdmin, self).get_exclude(request, obj)
        return ['merchant']

    # def save_form(self, request, form, change):
    #     if request.user.is_superuser or (request.user.is_staff and not request.user.is_merchant):
    #         return super().save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        if request.user.is_merchant:
            obj.merchant_id = request.user.merchant.id
            obj.save()

    def get_queryset(self, request):
        qs = super(MobileProductionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        print(request.user.id)
        merchant = Merchant.objects\
            .select_related('user')\
            .get(user_id=request.user.id)
        print(merchant.id)
        return MobileProduction.objects\
            .select_related('merchant')\
            .filter(merchant_id=merchant.id)
