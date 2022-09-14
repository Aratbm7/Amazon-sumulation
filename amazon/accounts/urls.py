from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('customers', views.CustomerViewset)


urlpatterns = router.urls
