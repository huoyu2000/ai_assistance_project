from rest_framework import serializers
from .models import Inventory, InventoryBatch, InventoryTransaction, InventoryCount, InventoryCountItem
from product.serializers import ProductSerializer

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'current_quantity', 'minimum_quantity', 
                 'maximum_quantity', 'updated_at', 'product_unit', 'is_low_stock']

class InventoryBatchSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    purchase_order_number = serializers.CharField(source='purchase_order_item.purchase_order.order_number', 
                                                 read_only=True, allow_null=True)
    
    class Meta:
        model = InventoryBatch
        fields = ['id', 'product', 'product_name', 'batch_number', 'quantity', 'remaining_quantity', 
                 'cost_price', 'production_date', 'expiry_date', 'purchase_order_item', 
                 'purchase_order_number', 'notes', 'created_at', 'product_unit', 'is_expired']

class InventoryTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True, allow_null=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    
    class Meta:
        model = InventoryTransaction
        fields = ['id', 'product', 'product_name', 'batch', 'batch_number', 'transaction_type', 
                 'transaction_type_display', 'quantity', 'unit_cost', 'reference_number', 
                 'notes', 'transaction_time', 'created_by', 'product_unit']

class InventoryCountItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    
    class Meta:
        model = InventoryCountItem
        fields = ['id', 'inventory_count', 'product', 'product_name', 'expected_quantity', 
                 'actual_quantity', 'difference', 'notes', 'product_unit']

class InventoryCountSerializer(serializers.ModelSerializer):
    items = InventoryCountItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = InventoryCount
        fields = ['id', 'count_number', 'count_date', 'status', 'status_display', 'notes', 
                 'created_by', 'created_at', 'completed_at', 'items']
    
    def create(self, validated_data):
        items_data = self.context.get('items', [])
        inventory_count = InventoryCount.objects.create(**validated_data)
        
        for item_data in items_data:
            expected_quantity = item_data.get('expected_quantity', 0)
            actual_quantity = item_data.get('actual_quantity', 0)
            item_data['difference'] = actual_quantity - expected_quantity
            
            InventoryCountItem.objects.create(inventory_count=inventory_count, **item_data)
        
        return inventory_count
    
    def update(self, instance, validated_data):
        items_data = self.context.get('items', None)
        
        # 更新盘点基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # 如果有提供盘点项数据，则更新
        if items_data is not None:
            # 删除现有项
            InventoryCountItem.objects.filter(inventory_count=instance).delete()
            
            # 添加新项
            for item_data in items_data:
                expected_quantity = item_data.get('expected_quantity', 0)
                actual_quantity = item_data.get('actual_quantity', 0)
                item_data['difference'] = actual_quantity - expected_quantity
                
                InventoryCountItem.objects.create(inventory_count=instance, **item_data)
        
        instance.save()
        return instance 