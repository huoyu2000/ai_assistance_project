from django.contrib import admin
from .models import Inventory, InventoryBatch, InventoryTransaction, InventoryCount, InventoryCountItem

admin.site.register(Inventory)
admin.site.register(InventoryBatch)
admin.site.register(InventoryTransaction)
admin.site.register(InventoryCount)
admin.site.register(InventoryCountItem)
