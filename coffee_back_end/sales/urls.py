from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 注册视图集
router.register(r'customers', views.CustomerViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'receipts', views.ReceiptViewSet)
router.register(r'drink-tickets', views.DrinkTicketViewSet)

urlpatterns = [
    # 其他URL模式将在这里添加
]

urlpatterns += router.urls 