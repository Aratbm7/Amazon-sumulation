from rest_framework_simplejwt import authentication
from .models import Merchant, Customer
from core.models import User
from django.contrib.auth.models import Group
# from django.http import QueryDict


class AccountsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # data = QueryDict(request.body)
        # print(data)accounts

        response = self.get_response(request)
        self.check_fields_is_full(request)

        return response

    def check_fields_is_full(self, request):
        if 'accounts/merchant/me' in request.path and request.method == 'PUT':
            request.user_id = authentication.JWTAuthentication().authenticate(request)[
                1]['user_id']
            customer = Customer.objects\
                .select_related('user')\
                .filter(user_id=request.user_id)
            merchant = Merchant.objects\
                .select_related('user')\
                .get(user_id=request.user_id)
            removed_list = ['id', 'is_active_in_merchant', 'user']
            merchant_fields = [f.name for f in Merchant._meta.get_fields() if (
                f.name not in removed_list)]
            fields_value = [getattr(merchant, name)
                            for name in merchant_fields]

            if "" not in fields_value:
                User.objects.filter(id=request.user_id).update(
                    is_merchant=True, is_staff=True)
                Merchant.objects.filter(user_id=request.user_id).update(
                    is_active_in_merchant=True)
                customer.update(is_merchant_user=True)

                # add merchant user to Merchant permission group
                user = User.objects.get(id=request.user_id)
                group = Group.objects.get(name='Merchants')
                group.user_set.add(user)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if authentication.JWTAuthentication().authenticate(request):
            request.user_id = authentication.JWTAuthentication().authenticate(request)[
                1]['user_id']

            if 'accounts/merchant/me' in request.path and\
                    not Merchant.objects.select_related('user').filter(user_id=request.user_id).exists():
                Merchant.objects.create(user_id=request.user_id)
