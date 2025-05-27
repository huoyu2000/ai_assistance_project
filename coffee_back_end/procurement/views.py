from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Supplier, SupplierProduct, PurchaseOrder, PurchaseOrderItem
from .serializers import (
    SupplierSerializer, SupplierProductSerializer,
    PurchaseOrderSerializer, PurchaseOrderItemSerializer
)

# Create your views here.

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'supplier_code', 'contact_person', 'phone', 'email']
    ordering_fields = ['name', 'supplier_code', 'created_at']
    
    def get_queryset(self):
        queryset = Supplier.objects.all()
        
        # 按活跃状态筛选
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """获取供应商提供的产品"""
        supplier = self.get_object()
        products = SupplierProduct.objects.filter(supplier=supplier)
        serializer = SupplierProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def purchase_orders(self, request, pk=None):
        """获取供应商的采购订单"""
        supplier = self.get_object()
        orders = PurchaseOrder.objects.filter(supplier=supplier)
        serializer = PurchaseOrderSerializer(orders, many=True)
        return Response(serializer.data)

class SupplierProductViewSet(viewsets.ModelViewSet):
    queryset = SupplierProduct.objects.all()
    serializer_class = SupplierProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = SupplierProduct.objects.all()
        
        # 按供应商筛选
        supplier = self.request.query_params.get('supplier', None)
        if supplier:
            queryset = queryset.filter(supplier__id=supplier)
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
        
        # 按首选供应商筛选
        is_preferred = self.request.query_params.get('is_preferred', None)
        if is_preferred is not None:
            is_preferred = is_preferred.lower() == 'true'
            queryset = queryset.filter(is_preferred=is_preferred)
            
        return queryset

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-order_date', 'order_number')
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_number', 'supplier__name', 'notes']
    ordering_fields = ['order_date', 'expected_delivery_date', 'status', 'total_amount']
    
    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        
        # 按状态筛选
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # 按供应商筛选
        supplier = self.request.query_params.get('supplier', None)
        if supplier:
            queryset = queryset.filter(supplier__id=supplier)
        
        # 按日期范围筛选
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(order_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(order_date__lte=end_date)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        items_data = request.data.pop('items', [])
        serializer = self.get_serializer(data=request.data, context={'items': items_data})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        items_data = request.data.pop('items', None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'items': items_data})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        """接收采购订单商品"""
        purchase_order = self.get_object()
        
        # 检查订单状态
        if purchase_order.status in ['closed', 'cancelled']:
            return Response({"detail": "无法接收已关闭或已取消的订单"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取接收的商品信息
        received_items = request.data.get('items', [])
        if not received_items:
            return Response({"detail": "未提供接收的商品信息"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新每个商品的接收数量
        fully_received = True
        for received_item in received_items:
            item_id = received_item.get('id')
            received_quantity = received_item.get('received_quantity', 0)
            
            try:
                order_item = PurchaseOrderItem.objects.get(id=item_id, purchase_order=purchase_order)
                
                # 累加接收数量
                order_item.received_quantity += received_quantity
                
                # 检查是否完全接收
                if order_item.received_quantity < order_item.quantity:
                    fully_received = False
                
                order_item.save()
                
            except PurchaseOrderItem.DoesNotExist:
                return Response({"detail": f"订单项 ID {item_id} 不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        # 更新订单状态
        if fully_received:
            purchase_order.status = 'fully_received'
        else:
            purchase_order.status = 'partially_received'
        
        purchase_order.save()
        
        # 返回更新后的订单
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)

class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = PurchaseOrderItem.objects.all()
        
        # 按采购订单筛选
        purchase_order = self.request.query_params.get('purchase_order', None)
        if purchase_order:
            queryset = queryset.filter(purchase_order__id=purchase_order)
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
            
        return queryset
