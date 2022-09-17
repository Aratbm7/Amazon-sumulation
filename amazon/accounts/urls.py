from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('customers', views.CustomerViewset)
router.register('merchant', views.MerchantViewset)


urlpatterns = router.urls
