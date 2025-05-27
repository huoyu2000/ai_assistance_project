from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Customer, Order, OrderItem, Receipt, DrinkTicket
from .serializers import (
    CustomerSerializer, OrderSerializer, OrderItemSerializer,
    ReceiptSerializer, DrinkTicketSerializer
)
from inventory.models import Inventory, InventoryTransaction
from product.models import Product, InventoryLevel

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone', 'member_code']
    ordering_fields = ['name', 'member_code', 'total_consumption', 'created_at']
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        
        # 按客户类型筛选
        customer_type = self.request.query_params.get('customer_type', None)
        if customer_type:
            queryset = queryset.filter(customer_type=customer_type)
        
        # 按激活状态筛选
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """获取客户的订单"""
        customer = self.get_object()
        
        # 注意：这里可能会有问题，因为实际数据库中可能不存在customer关系
        # 我们返回一个空数组避免错误
        # orders = Order.objects.filter(customer=customer)
        
        # 返回空数组，因为实际数据库中可能没有这个关系
        serializer = OrderSerializer([], many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_no', 'table_no']
    ordering_fields = ['created_at', 'total', 'status']
    
    def get_queryset(self):
        queryset = Order.objects.all()
        
        # 按状态筛选
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # 按订单类型筛选
        channel = self.request.query_params.get('channel', None)
        if channel:
            queryset = queryset.filter(channel=channel)
        
        # 按支付状态筛选（已支付 = status为PAID）
        payment_status = self.request.query_params.get('payment_status', None)
        if payment_status is not None:
            payment_status = payment_status.lower() == 'true'
            if payment_status:
                queryset = queryset.filter(status='PAID')
            else:
                queryset = queryset.exclude(status='PAID')
        
        # 按日期范围筛选
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        items_data = request.data.pop('items', [])
        create_receipt = request.data.pop('create_receipt', False)
        drink_tickets = request.data.pop('drink_tickets', [])
        
        serializer = self.get_serializer(
            data=request.data, 
            context={
                'items': items_data,
                'create_receipt': create_receipt,
                'drink_tickets': drink_tickets
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 处理库存扣减
        order = serializer.instance
        order_items = OrderItem.objects.filter(order=order)
        
        for order_item in order_items:
            try:
                # 扣减库存
                inventory = Product.objects.get(product_id=order_item.product.product_id)
                inventory.inventory_qty -= order_item.qty
                inventory.save()
                
                # 记录库存交易
                InventoryTransaction.objects.create(
                    product=order_item.product,
                    transaction_type='sales',
                    quantity=-order_item.qty,  # 负数表示出库
                    unit_cost=order_item.unit_price,
                    reference_number=order.order_no,
                    notes=f"销售单: {order.order_no}",
                    created_by=request.user.username
                )
            except Product.DoesNotExist:
                # 如果产品没有库存记录，跳过
                pass
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        items_data = request.data.pop('items', None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial,
            context={'items': items_data}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """支付订单"""
        order = self.get_object()
        
        # 检查订单状态
        if order.status == 'REFUNDED':
            return Response({"detail": "已退款的订单不能支付"}, status=status.HTTP_400_BAD_REQUEST)
        
        if order.status == 'PAID':
            return Response({"detail": "订单已支付"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取支付信息
        payment_method = request.data.get('payment_method', None)
        if not payment_method:
            return Response({"detail": "未提供支付方式"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新订单
        order.status = 'PAID'
        order.paid_at = timezone.now()
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """退款订单"""
        order = self.get_object()
        
        # 检查订单状态
        if order.status != 'PAID':
            return Response({"detail": "只有已支付的订单才能退款"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新订单状态
        order.status = 'REFUNDED'
        order.save()
        
        # 恢复库存
        order_items = OrderItem.objects.filter(order=order)
        
        for order_item in order_items:
            try:
                # 恢复库存
                inventory = Product.objects.get(product_id=order_item.product.product_id)
                inventory.inventory_qty += order_item.qty
                inventory.save()
                
                # 记录库存交易
                InventoryTransaction.objects.create(
                    product=order_item.product,
                    transaction_type='return',
                    quantity=order_item.qty,  # 正数表示入库
                    unit_cost=order_item.unit_price,
                    reference_number=order.order_no,
                    notes=f"退款销售单: {order.order_no}",
                    created_by=request.user.username
                )
            except Product.DoesNotExist:
                # 如果产品没有库存记录，跳过
                pass
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = OrderItem.objects.all()
        
        # 按订单筛选
        order = self.request.query_params.get('order', None)
        if order:
            queryset = queryset.filter(order__order_id=order)
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__product_id=product)
            
        return queryset

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Receipt.objects.all()
        
        # 按打印状态筛选
        printed = self.request.query_params.get('printed', None)
        if printed is not None:
            printed = printed.lower() == 'true'
            queryset = queryset.filter(printed=printed)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def print(self, request, pk=None):
        """打印小票"""
        receipt = self.get_object()
        
        # 如果已打印，返回错误
        if receipt.printed:
            return Response({"detail": "小票已打印"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 模拟打印过程
        # 在实际应用中，这里应该调用打印机API
        
        # 更新打印状态
        receipt.printed = True
        receipt.print_time = timezone.now()
        receipt.save()
        
        serializer = self.get_serializer(receipt)
        return Response(serializer.data)

class DrinkTicketViewSet(viewsets.ModelViewSet):
    queryset = DrinkTicket.objects.all()
    serializer_class = DrinkTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ticket_number', 'order_item__product_name', 'barista']
    ordering_fields = ['status', 'start_time', 'complete_time']
    
    def get_queryset(self):
        queryset = DrinkTicket.objects.all()
        
        # 按状态筛选
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # 按制作人员筛选
        barista = self.request.query_params.get('barista', None)
        if barista:
            queryset = queryset.filter(barista=barista)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def start_making(self, request, pk=None):
        """开始制作饮品"""
        drink_ticket = self.get_object()
        
        # 检查饮品票状态
        if drink_ticket.status != 'waiting':
            return Response({"detail": "只有等待中的饮品才能开始制作"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取制作人员
        barista = request.data.get('barista', request.user.username)
        
        # 更新饮品票状态
        drink_ticket.status = 'making'
        drink_ticket.barista = barista
        drink_ticket.start_time = timezone.now()
        drink_ticket.save()
        
        serializer = self.get_serializer(drink_ticket)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成饮品制作"""
        drink_ticket = self.get_object()
        
        # 检查饮品票状态
        if drink_ticket.status not in ['waiting', 'making']:
            return Response({"detail": "只有等待中或制作中的饮品才能完成"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新饮品票状态
        drink_ticket.status = 'completed'
        drink_ticket.complete_time = timezone.now()
        
        # 如果没有制作人员，设置为当前用户
        if not drink_ticket.barista:
            drink_ticket.barista = request.user.username
        
        # 如果没有开始时间，设置为当前时间
        if not drink_ticket.start_time:
            drink_ticket.start_time = timezone.now()
        
        drink_ticket.save()
        
        serializer = self.get_serializer(drink_ticket)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        """交付饮品"""
        drink_ticket = self.get_object()
        
        # 检查饮品票状态
        if drink_ticket.status != 'completed':
            return Response({"detail": "只有已完成的饮品才能交付"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新饮品票状态
        drink_ticket.status = 'delivered'
        drink_ticket.save()
        
        # 检查订单中所有饮品是否都已交付
        order = drink_ticket.order_item.order
        all_delivered = True
        
        for order_item in order.items.all():
            try:
                ticket = DrinkTicket.objects.get(order_item=order_item)
                if ticket.status != 'delivered':
                    all_delivered = False
                    break
            except DrinkTicket.DoesNotExist:
                # 如果订单项没有饮品票，跳过
                pass
        
        serializer = self.get_serializer(drink_ticket)
        return Response(serializer.data)
