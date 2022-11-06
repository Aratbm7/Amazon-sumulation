from .serializers import CategorySerializer, MobileProductSerilizers, SubcategorySerializers
from rest_framework_simplejwt import authentication
from rest_framework.viewsets import ModelViewSet
from .paginations import CategoryPagination
from .permissions import IsAdminUserAndNotMerchantOrReadOnly
from .models import Category, MobileProduction, SubCategory
from accounts.models import Merchant


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserAndNotMerchantOrReadOnly]
    pagination_class = CategoryPagination

    def get_serializer_context(self):
        return {'scheme': self.request.scheme, 'domain': self.request.META["HTTP_HOST"]}


class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubcategorySerializers
    permission_classes = [IsAdminUserAndNotMerchantOrReadOnly]
    pagination_class = CategoryPagination

    def get_queryset(self):
        return SubCategory.objects\
            .prefetch_related('products')\
            .filter(category_id=self.kwargs['category_pk'])

    def get_serializer_context(self):
        return {'category_id': self.kwargs['category_pk'],
                'scheme': self.request.scheme, 'domain': self.request.META["HTTP_HOST"]}


class MobileProductViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'delete', 'header', 'option']
    queryset = MobileProduction.objects\
        .prefetch_related('images')\
        .select_related('merchant')\
        .select_related('subcategory')\
        .all()
    serializer_class = MobileProductSerilizers
    permission_classes = [IsAdminUserAndNotMerchantOrReadOnly]

    def get_merchant_id(self):
        merchant_id = None
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            merchant = Merchant.objects\
                .select_related('user')\
                .get(user_id=self.request.user.id)
            merchant_id = getattr(merchant, 'id')
        return merchant_id

    def get_serializer_context(self):
        return {'merchant_id': self.get_merchant_id(),
                'scheme': self.request.scheme, 'domain': self.request.META["HTTP_HOST"]}
