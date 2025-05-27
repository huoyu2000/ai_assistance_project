from rest_framework import serializers
from .models import Supplier, SupplierProduct, PurchaseOrder, PurchaseOrderItem
from product.serializers import ProductSerializer

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    
    class Meta:
        model = SupplierProduct
        fields = ['id', 'supplier', 'supplier_name', 'product', 'product_name', 
                 'supplier_product_code', 'price', 'min_order_quantity', 'lead_time_days',
                 'is_preferred', 'contract_start_date', 'contract_end_date', 
                 'created_at', 'updated_at', 'product_unit']

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'purchase_order', 'product', 'product_name', 'quantity', 
                 'unit_price', 'subtotal', 'received_quantity', 'notes', 'product_unit']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'supplier_name', 'order_date', 
                 'expected_delivery_date', 'status', 'total_amount', 'payment_terms', 
                 'notes', 'created_by', 'created_at', 'updated_at', 'items']
    
    def create(self, validated_data):
        items_data = self.context.get('items', [])
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in items_data:
            quantity = item_data.get('quantity', 0)
            unit_price = item_data.get('unit_price', 0)
            subtotal = quantity * unit_price
            item_data['subtotal'] = subtotal
            total_amount += subtotal
            
            PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)
        
        # 更新总金额
        purchase_order.total_amount = total_amount
        purchase_order.save()
        
        return purchase_order
    
    def update(self, instance, validated_data):
        items_data = self.context.get('items', None)
        
        # 更新采购订单基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # 如果有提供订单项数据，则更新
        if items_data is not None:
            # 删除现有项
            PurchaseOrderItem.objects.filter(purchase_order=instance).delete()
            
            # 添加新项并重新计算总金额
            total_amount = 0
            for item_data in items_data:
                quantity = item_data.get('quantity', 0)
                unit_price = item_data.get('unit_price', 0)
                subtotal = quantity * unit_price
                item_data['subtotal'] = subtotal
                total_amount += subtotal
                
                PurchaseOrderItem.objects.create(purchase_order=instance, **item_data)
            
            # 更新总金额
            instance.total_amount = total_amount
        
        instance.save()
        return instance 