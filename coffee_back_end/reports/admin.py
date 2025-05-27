from django.contrib import admin
from .models import SalesReport, TopSellingProduct, CustomerFlowHeatmap, MemberRepurchaseRate

admin.site.register(SalesReport)
admin.site.register(TopSellingProduct)
admin.site.register(CustomerFlowHeatmap)
admin.site.register(MemberRepurchaseRate)
