from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework_simplejwt import authentication
from accounts.models import Merchant


class IsAdminUserAndNotMerchantOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and
             request.user.is_staff) and
            not request.user.is_merchant
        )


# class IsAdminUserOrIsMerchantOrReadOnly(BasePermission):

#     def get_merchant(self, request):
#         merchant_value = False
#         if request.user.is_authenticated:
#             request.user_id = authentication.JWTTokenUserAuthentication(
#             ).authenticate(request)[1]['user_id']
#             merchant = Merchant.objects\
#                 .select_related('user')\
#                 .get(user_id=request.user_id)
#             merchant_value = getattr(merchant, 'is_active_in_merchant')
#             print(merchant_value)
#         return merchant_value

#     def gat_safe_method(self, request):
#         if request.method in SAFE_METHODS:
#             return True
#         return False

#     def has_permission(self, request, view):

#         return bool(
#             self.gat_safe_method(request) or
#             self.get_merchant(request) or (request.user and request.user.is_staff))
