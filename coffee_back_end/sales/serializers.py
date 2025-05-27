from rest_framework import serializers
from .models import Customer, Order, OrderItem, Receipt, DrinkTicket
from product.models import Product

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['item_id', 'order', 'product', 'product_name', 'qty', 'unit_price', 'line_total']

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class DrinkTicketSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='order_item.product.name', read_only=True)
    order_number = serializers.CharField(source='order_item.order.order_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = DrinkTicket
        fields = ['id', 'order_item', 'ticket_number', 'status', 'status_display', 
                 'barista', 'start_time', 'complete_time', 'notes', 'product_name', 'order_number']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.SerializerMethodField()
    receipt_number = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['order_id', 'order_no', 'customer', 'customer_name', 'channel', 
                 'table_no', 'subtotal', 'tax', 'total', 'status', 
                 'payment_method', 'paid_at', 'created_by', 'created_at', 'items', 'receipt_number']
    
    def get_customer_name(self, obj):
        try:
            if hasattr(obj, 'customer') and obj.customer:
                return obj.customer.name
        except:
            pass
        return None
    
    def get_receipt_number(self, obj):
        try:
            if hasattr(obj, 'receipt'):
                return obj.receipt.receipt_number
        except:
            pass
        return None
    
    def create(self, validated_data):
        items_data = self.context.get('items', [])
        order = Order.objects.create(**validated_data)
        
        # 创建订单项
        for item_data in items_data:
            product_id = item_data.get('product')
            qty = item_data.get('qty', 1)
            unit_price = item_data.get('unit_price', 0)
            product_name = item_data.get('product_name', '')
            
            # 如果没有提供单价或产品名称，尝试从产品获取
            try:
                product = Product.objects.get(pk=product_id)
                if not product_name:
                    product_name = product.name
                if not unit_price:
                    unit_price = product.price
            except Product.DoesNotExist:
                pass
            
            # 计算行总价
            line_total = float(qty) * float(unit_price)
            
            # 创建订单项
            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                product_name=product_name,
                qty=qty,
                unit_price=unit_price,
                line_total=line_total
            )
        
        # 创建小票（如果需要）
        if self.context.get('create_receipt', False):
            receipt_number = f"R{order.order_no}"
            Receipt.objects.create(
                order=order,
                receipt_number=receipt_number,
                printed=False
            )
        
        return order
    
    def update(self, instance, validated_data):
        items_data = self.context.get('items', None)
        
        # 更新订单基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 如果有提供订单项数据，则更新
        if items_data is not None:
            # 删除现有项
            OrderItem.objects.filter(order=instance).delete()
            
            # 添加新项
            for item_data in items_data:
                product_id = item_data.get('product')
                qty = item_data.get('qty', 1)
                unit_price = item_data.get('unit_price', 0)
                product_name = item_data.get('product_name', '')
                
                # 如果没有提供单价或产品名称，尝试从产品获取
                try:
                    product = Product.objects.get(pk=product_id)
                    if not product_name:
                        product_name = product.name
                    if not unit_price:
                        unit_price = product.price
                except Product.DoesNotExist:
                    pass
                
                # 计算行总价
                line_total = float(qty) * float(unit_price)
                
                # 创建订单项
                OrderItem.objects.create(
                    order=instance,
                    product_id=product_id,
                    product_name=product_name,
                    qty=qty,
                    unit_price=unit_price,
                    line_total=line_total
                )
        
        return instance 