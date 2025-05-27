from rest_framework import serializers
from .models import Category, Product, Recipe, RecipeItem, PromotionalPrice, TimeSlotPrice, InventoryLevel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'sort_order', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'sku', 'category', 'category_name', 
                 'unit', 'price', 'inventory_qty', 'reorder_point', 
                 'status', 'stock_status', 'created_at', 'updated_at']

class RecipeItemSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    ingredient_unit = serializers.CharField(source='ingredient.unit', read_only=True)
    
    class Meta:
        model = RecipeItem
        fields = ['id', 'ingredient', 'ingredient_name', 'quantity', 'unit', 'ingredient_unit']

class RecipeSerializer(serializers.ModelSerializer):
    recipe_items = RecipeItemSerializer(many=True, read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'product', 'product_name', 'preparation_steps', 'recipe_items', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        recipe_items_data = self.context.get('recipe_items', [])
        recipe = Recipe.objects.create(**validated_data)
        
        for item_data in recipe_items_data:
            RecipeItem.objects.create(recipe=recipe, **item_data)
        
        return recipe

class PromotionalPriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = PromotionalPrice
        fields = ['id', 'product', 'product_name', 'name', 'price', 'start_time', 'end_time', 
                 'is_active', 'created_at', 'is_current']

class TimeSlotPriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = TimeSlotPrice
        fields = ['id', 'product', 'product_name', 'name', 'price', 'days_of_week', 
                 'start_time', 'end_time', 'is_active', 'created_at']

class InventoryLevelSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = InventoryLevel
        fields = ['product', 'product_name', 'stock_qty', 'unit', 
                 'reorder_point', 'is_low_stock', 'last_updated'] 