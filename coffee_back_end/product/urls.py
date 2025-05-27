from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 注册视图集
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'recipe-items', views.RecipeItemViewSet)
router.register(r'promotional-prices', views.PromotionalPriceViewSet)
router.register(r'time-slot-prices', views.TimeSlotPriceViewSet)

urlpatterns = [
    # 其他URL模式将在这里添加
]

urlpatterns += router.urls 