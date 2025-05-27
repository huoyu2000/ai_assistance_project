from django.contrib import admin
from .models import Supplier, SupplierProduct, PurchaseOrder, PurchaseOrderItem

admin.site.register(Supplier)
admin.site.register(SupplierProduct)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
