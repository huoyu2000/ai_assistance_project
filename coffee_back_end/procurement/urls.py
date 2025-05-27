from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 注册视图集
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'supplier-products', views.SupplierProductViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'purchase-order-items', views.PurchaseOrderItemViewSet)

urlpatterns = [
    # 其他URL模式将在这里添加
]

urlpatterns += router.urls 