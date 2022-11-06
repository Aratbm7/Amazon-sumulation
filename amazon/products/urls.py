from rest_framework_nested import routers
from .views import CategoryViewSet, MobileProductViewSet, SubCategoryViewSet

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('products', MobileProductViewSet, basename='products')
category_roter = routers.NestedDefaultRouter(
    router, 'categories', lookup='category')

category_roter.register('subcategories', SubCategoryViewSet,
                        basename='category_subcategories')

urlpatterns = router.urls + category_roter.urls
