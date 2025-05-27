from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 注册视图集
router.register(r'daily-revenue', views.DailyRevenueViewSet)
router.register(r'costs', views.CostRecordViewSet)
router.register(r'profit-reports', views.ProfitReportViewSet)

urlpatterns = [
    # 其他URL模式将在这里添加
]

urlpatterns += router.urls 