from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from django.utils import timezone
from .models import Inventory, InventoryBatch, InventoryTransaction, InventoryCount, InventoryCountItem
from .serializers import (
    InventorySerializer, InventoryBatchSerializer, InventoryTransactionSerializer,
    InventoryCountSerializer, InventoryCountItemSerializer
)
from product.models import Product

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product__name', 'product__product_code']
    ordering_fields = ['product__name', 'current_quantity', 'updated_at']
    
    def get_queryset(self):
        queryset = Inventory.objects.all()
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
        
        # 按库存水平筛选
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None:
            low_stock = low_stock.lower() == 'true'
            if low_stock:
                # 查找库存低于最低库存量的产品
                queryset = queryset.filter(current_quantity__lte=F('minimum_quantity'))
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def adjust(self, request, pk=None):
        """调整库存数量"""
        inventory = self.get_object()
        quantity = request.data.get('quantity', 0)
        notes = request.data.get('notes', '')
        created_by = request.data.get('created_by', request.user.username)
        
        if quantity == 0:
            return Response({"detail": "调整数量不能为0"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 调整库存
        inventory.current_quantity += quantity
        inventory.save()
        
        # 记录交易
        transaction_type = 'adjustment'
        InventoryTransaction.objects.create(
            product=inventory.product,
            transaction_type=transaction_type,
            quantity=quantity,
            unit_cost=inventory.product.cost_price,
            notes=notes,
            created_by=created_by
        )
        
        serializer = self.get_serializer(inventory)
        return Response(serializer.data)

class InventoryBatchViewSet(viewsets.ModelViewSet):
    queryset = InventoryBatch.objects.all()
    serializer_class = InventoryBatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['batch_number', 'product__name', 'notes']
    ordering_fields = ['expiry_date', 'created_at', 'remaining_quantity']
    
    def get_queryset(self):
        queryset = InventoryBatch.objects.all()
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
        
        # 按过期状态筛选
        expired = self.request.query_params.get('expired', None)
        if expired is not None:
            expired = expired.lower() == 'true'
            today = timezone.now().date()
            if expired:
                queryset = queryset.filter(expiry_date__lt=today)
            else:
                queryset = queryset.filter(expiry_date__gte=today)
        
        # 按即将过期筛选（30天内）
        expiring_soon = self.request.query_params.get('expiring_soon', None)
        if expiring_soon is not None:
            expiring_soon = expiring_soon.lower() == 'true'
            if expiring_soon:
                today = timezone.now().date()
                thirty_days_later = today + timezone.timedelta(days=30)
                queryset = queryset.filter(expiry_date__gte=today, expiry_date__lte=thirty_days_later)
        
        # 按剩余数量筛选
        has_remaining = self.request.query_params.get('has_remaining', None)
        if has_remaining is not None:
            has_remaining = has_remaining.lower() == 'true'
            if has_remaining:
                queryset = queryset.filter(remaining_quantity__gt=0)
            else:
                queryset = queryset.filter(remaining_quantity=0)
            
        return queryset

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product__name', 'reference_number', 'notes', 'created_by']
    ordering_fields = ['transaction_time', 'product__name', 'quantity']
    
    def get_queryset(self):
        queryset = InventoryTransaction.objects.all()
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
        
        # 按批次筛选
        batch = self.request.query_params.get('batch', None)
        if batch:
            queryset = queryset.filter(batch__id=batch)
        
        # 按交易类型筛选
        transaction_type = self.request.query_params.get('transaction_type', None)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # 按日期范围筛选
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(transaction_time__date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(transaction_time__date__lte=end_date)
            
        return queryset

class InventoryCountViewSet(viewsets.ModelViewSet):
    queryset = InventoryCount.objects.all()
    serializer_class = InventoryCountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['count_number', 'notes', 'created_by']
    ordering_fields = ['count_date', 'status', 'created_at']
    
    def get_queryset(self):
        queryset = InventoryCount.objects.all()
        
        # 按状态筛选
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # 按日期范围筛选
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(count_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(count_date__lte=end_date)
            
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
    def complete(self, request, pk=None):
        """完成盘点并应用库存调整"""
        inventory_count = self.get_object()
        
        # 检查盘点状态
        if inventory_count.status not in ['draft', 'in_progress']:
            return Response({"detail": "只有草稿或进行中的盘点才能完成"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取盘点项
        count_items = InventoryCountItem.objects.filter(inventory_count=inventory_count)
        if not count_items.exists():
            return Response({"detail": "盘点没有任何项目"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 应用库存调整
        for item in count_items:
            try:
                inventory = Inventory.objects.get(product=item.product)
                
                # 计算差异并调整库存
                adjustment = item.actual_quantity - inventory.current_quantity
                if adjustment != 0:
                    inventory.current_quantity = item.actual_quantity
                    inventory.save()
                    
                    # 记录交易
                    InventoryTransaction.objects.create(
                        product=item.product,
                        transaction_type='adjustment',
                        quantity=adjustment,
                        unit_cost=item.product.cost_price,
                        reference_number=inventory_count.count_number,
                        notes=f"盘点调整：{inventory_count.count_number}",
                        created_by=request.user.username
                    )
            except Inventory.DoesNotExist:
                # 如果库存记录不存在，则创建
                if item.actual_quantity > 0:
                    inventory = Inventory.objects.create(
                        product=item.product,
                        current_quantity=item.actual_quantity,
                        minimum_quantity=10,  # 默认值
                        maximum_quantity=100  # 默认值
                    )
                    
                    # 记录交易
                    InventoryTransaction.objects.create(
                        product=item.product,
                        transaction_type='adjustment',
                        quantity=item.actual_quantity,
                        unit_cost=item.product.cost_price,
                        reference_number=inventory_count.count_number,
                        notes=f"盘点初始化：{inventory_count.count_number}",
                        created_by=request.user.username
                    )
        
        # 更新盘点状态
        inventory_count.status = 'completed'
        inventory_count.completed_at = timezone.now()
        inventory_count.save()
        
        serializer = self.get_serializer(inventory_count)
        return Response(serializer.data)

class InventoryCountItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryCountItem.objects.all()
    serializer_class = InventoryCountItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = InventoryCountItem.objects.all()
        
        # 按盘点ID筛选
        inventory_count = self.request.query_params.get('inventory_count', None)
        if inventory_count:
            queryset = queryset.filter(inventory_count__id=inventory_count)
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
            
        return queryset

# 新增库存预警API视图集
class InventoryAlertsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='low_stock')
    def low_stock(self, request):
        """获取低库存预警"""
        low_stock_items = Inventory.objects.filter(current_quantity__lte=F('minimum_quantity'))
        serializer = InventorySerializer(low_stock_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='expiring_soon')
    def expiring_soon(self, request):
        """获取即将过期预警（30天内）"""
        today = timezone.now().date()
        thirty_days_later = today + timezone.timedelta(days=30)
        
        expiring_batches = InventoryBatch.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=thirty_days_later,
            status='ACTIVE'
        )
        serializer = InventoryBatchSerializer(expiring_batches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        """获取所有库存预警"""
        # 获取低库存预警
        low_stock_items = Inventory.objects.filter(current_quantity__lte=F('minimum_quantity'))
        low_stock_serializer = InventorySerializer(low_stock_items, many=True)
        
        # 获取即将过期预警
        today = timezone.now().date()
        thirty_days_later = today + timezone.timedelta(days=30)
        
        expiring_batches = InventoryBatch.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=thirty_days_later,
            status='ACTIVE'
        )
        expiring_serializer = InventoryBatchSerializer(expiring_batches, many=True)
        
        return Response({
            'low_stock': low_stock_serializer.data,
            'expiring_soon': expiring_serializer.data
        })
