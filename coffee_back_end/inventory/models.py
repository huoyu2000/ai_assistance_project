from django.db import models
from django.utils import timezone
from product.models import Product, InventoryLevel
from procurement.models import PurchaseOrder, PurchaseOrderItem

class Inventory(models.Model):
    """库存模型"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory', verbose_name='商品')
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='当前库存量')
    minimum_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=10, verbose_name='最低库存量')
    maximum_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=100, verbose_name='最高库存量')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '库存'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.product.name} - 当前库存: {self.current_quantity}{self.product.unit}"
    
    def is_low_stock(self):
        """检查是否低库存"""
        return self.current_quantity <= self.minimum_quantity

class InventoryBatch(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', '活跃'),
        ('EXPIRED', '已过期'),
        ('USED_UP', '已用完')
    ]
    
    batch_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, models.CASCADE, db_column='product_id')
    batch_no = models.CharField(max_length=32)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'inventory_batches'
        verbose_name = '库存批次'
        verbose_name_plural = '库存批次'
        ordering = ['expiry_date', 'batch_no']

    def __str__(self):
        return f"{self.product.name} - {self.batch_no}"
    
    @property
    def is_expired(self):
        if not self.expiry_date:
            return False
        return self.expiry_date < timezone.now().date()
    
    @property
    def remaining_quantity(self):
        return self.qty

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', '采购入库'),
        ('sales', '销售出库'),
        ('return', '退货入库'),
        ('adjustment', '库存调整'),
        ('transfer', '库存转移'),
        ('production', '生产'),
        ('consumption', '消耗'),
        ('loss', '报损'),
        ('expiry', '过期'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, models.CASCADE, related_name='transactions')
    batch = models.ForeignKey(InventoryBatch, models.SET_NULL, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference_number = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    transaction_time = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'inventory_transactions'
        verbose_name = '库存交易'
        verbose_name_plural = '库存交易'
        ordering = ['-transaction_time']

    def __str__(self):
        return f"{self.product.name} - {self.get_transaction_type_display()} - {self.quantity}"

class InventoryCount(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消')
    ]
    
    id = models.BigAutoField(primary_key=True)
    count_number = models.CharField(max_length=20, unique=True)
    count_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'inventory_counts'
        verbose_name = '库存盘点'
        verbose_name_plural = '库存盘点'
        ordering = ['-count_date', 'count_number']

    def __str__(self):
        return self.count_number

class InventoryCountItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    inventory_count = models.ForeignKey(InventoryCount, models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, models.CASCADE)
    expected_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    difference = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'inventory_count_items'
        verbose_name = '库存盘点项'
        verbose_name_plural = '库存盘点项'
        unique_together = ('inventory_count', 'product')

    def __str__(self):
        return f"{self.inventory_count.count_number} - {self.product.name}"
