from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 注册视图集
router.register(r'inventories', views.InventoryViewSet)
router.register(r'batches', views.InventoryBatchViewSet)
router.register(r'transactions', views.InventoryTransactionViewSet)
router.register(r'counts', views.InventoryCountViewSet)
router.register(r'count-items', views.InventoryCountItemViewSet)
router.register(r'stock-alerts', views.InventoryAlertsViewSet, basename='stock-alerts')

urlpatterns = [
    # 其他URL模式将在这里添加
]

urlpatterns += router.urls 