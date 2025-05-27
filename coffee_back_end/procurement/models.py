from django.db import models
from product.models import Product

class Supplier(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', '活跃'),
        ('INACTIVE', '停用')
    ]
    
    supplier_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    category = models.CharField(max_length=32, blank=True, null=True)
    contact_name = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')
    address = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'suppliers'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'
        ordering = ['name']

    def __str__(self):
        return self.name

# 采购订单相关模型需要根据需要自定义，因为原始数据表中没有
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('submitted', '已提交'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('ordered', '已下单'),
        ('partially_received', '部分收货'),
        ('fully_received', '完全收货'),
        ('cancelled', '已取消'),
        ('closed', '已关闭')
    ]
    
    order_id = models.BigAutoField(primary_key=True)
    order_number = models.CharField(max_length=32, unique=True)
    supplier = models.ForeignKey(Supplier, models.CASCADE)
    order_date = models.DateField()
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_terms = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True  # 自定义表
        db_table = 'purchase_orders'
        verbose_name = '采购订单'
        verbose_name_plural = '采购订单'
        ordering = ['-order_date', 'order_number']

    def __str__(self):
        return self.order_number

class PurchaseOrderItem(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    purchase_order = models.ForeignKey(PurchaseOrder, models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        managed = True  # 自定义表
        db_table = 'purchase_order_items'
        verbose_name = '采购订单项'
        verbose_name_plural = '采购订单项'

    def __str__(self):
        return f"{self.purchase_order.order_number} - {self.product.name}"

class SupplierProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, models.CASCADE, related_name='suppliers')
    supplier_product_code = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    lead_time_days = models.IntegerField(default=7)
    is_preferred = models.BooleanField(default=False)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True  # 自定义表
        db_table = 'supplier_products'
        verbose_name = '供应商产品'
        verbose_name_plural = '供应商产品'
        unique_together = ('supplier', 'product')

    def __str__(self):
        return f"{self.supplier.name} - {self.product.name}"
