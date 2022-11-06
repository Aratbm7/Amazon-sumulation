from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserAndNotMerchant(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            (request.user and
             request.user.is_staff) and
            not request.user.is_merchant
        )
