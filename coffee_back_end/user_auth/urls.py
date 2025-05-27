from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
# 注册视图集
router.register(r'staff', views.StaffViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'role-permissions', views.RolePermissionViewSet)
router.register(r'operation-logs', views.OperationLogViewSet)

urlpatterns = [
    # JWT认证相关URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls 