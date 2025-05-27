from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 注册视图集将在这里添加

urlpatterns = [
    # 其他URL模式将在这里添加
]

urlpatterns += router.urls 