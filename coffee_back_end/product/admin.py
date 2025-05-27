from django.contrib import admin
from .models import Category, Product, Recipe, RecipeItem, PromotionalPrice, TimeSlotPrice

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(RecipeItem)
admin.site.register(PromotionalPrice)
admin.site.register(TimeSlotPrice)
