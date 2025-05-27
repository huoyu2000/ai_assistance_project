from django.contrib import admin
from .models import DailyRevenue, CostRecord, ProfitReport

admin.site.register(DailyRevenue)
admin.site.register(CostRecord)
admin.site.register(ProfitReport)
