from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views
from .views import (
    StaffViewSet, PermissionViewSet, RoleViewSet, 
    RolePermissionViewSet, OperationLogViewSet,
    login_view, health_check
)

router = DefaultRouter()
# 注册视图集
router.register(r'staff', StaffViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'role-permissions', RolePermissionViewSet)
router.register(r'operation-logs', OperationLogViewSet)

urlpatterns = [
    # JWT认证相关URL
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 健康检查路由 - 放在最前面确保容易访问
    path('health/', health_check, name='health_check'),
]

urlpatterns += router.urls 