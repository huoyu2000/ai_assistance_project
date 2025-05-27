from django.db import models
from django.utils import timezone
from product.models import Product
from user_auth.models import Staff

class Customer(models.Model):
    """客户模型，根据需求自定义，原始数据库中不存在"""
    CUSTOMER_TYPES = [
        ('regular', '普通顾客'),
        ('member', '会员'),
        ('vip', 'VIP会员'),
        ('wholesale', '批发客户'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='regular')
    member_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    points = models.IntegerField(default=0)
    total_consumption = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'customers'
        verbose_name = '客户'
        verbose_name_plural = '客户'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Order(models.Model):
    """订单模型"""
    ORDER_TYPES = [
        ('DINE_IN', '堂食'),
        ('TAKE_AWAY', '外带'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', '开单'),
        ('PAID', '已支付'),
        ('REFUNDED', '已退款'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', '现金'),
        ('wechat', '微信'),
        ('alipay', '支付宝'),
        ('credit_card', '信用卡'),
        ('member_card', '会员卡'),
    ]
    
    order_id = models.BigAutoField(primary_key=True)
    order_no = models.CharField(max_length=32, unique=True)
    table_no = models.CharField(max_length=8, null=True, blank=True)
    channel = models.CharField(max_length=10, choices=ORDER_TYPES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_by = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # 映射到已有表中不存在的自定义字段 - 修改为使用不参与SQL查询的关系
    # 实际数据库中不存在customer_id字段，所以在访问这些字段时需要在应用层处理
    # 我们使用related_name+来指示Django不要创建反向关系
    customer = models.ForeignKey(
        Customer, 
        models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders',
        db_constraint=False,   # 不创建数据库约束
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True, blank=True)
    
    class Meta:
        managed = True
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.order_no
    
    @property
    def order_type(self):
        return self.channel
    
    @property
    def order_date(self):
        return self.created_at
    
    @property
    def total_amount(self):
        return self.total
    
    @property
    def payment_status(self):
        return self.status == 'PAID'
    
    @property
    def payment_time(self):
        return self.paid_at
    
    @property
    def cashier(self):
        return self.created_by

class OrderItem(models.Model):
    """订单项模型"""
    item_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, models.CASCADE, db_column='order_id', related_name='items')
    product = models.ForeignKey(Product, models.CASCADE, db_column='product_id')
    product_name = models.CharField(max_length=64)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        managed = True
        db_table = 'order_items'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
    
    def __str__(self):
        return f"{self.order.order_no} - {self.product_name}"
    
    @property
    def quantity(self):
        return self.qty
    
    @property
    def subtotal(self):
        return self.line_total
    
    @property
    def discount(self):
        return 0  # 原始表中没有折扣字段，默认为0

# 以下为自定义表，原始数据库中不存在
class Receipt(models.Model):
    """小票模型"""
    id = models.BigAutoField(primary_key=True)
    order = models.OneToOneField(Order, models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True)
    printed = models.BooleanField(default=False)
    print_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        managed = True
        db_table = 'receipts'
        verbose_name = '小票'
        verbose_name_plural = '小票'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.receipt_number

class DrinkTicket(models.Model):
    """饮品票模型"""
    STATUS_CHOICES = [
        ('waiting', '等待制作'),
        ('making', '制作中'),
        ('completed', '已完成'),
        ('delivered', '已交付'),
        ('cancelled', '已取消'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    order_item = models.OneToOneField(OrderItem, models.CASCADE, related_name='drink_ticket')
    ticket_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    barista = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    complete_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        managed = True
        db_table = 'drink_tickets'
        verbose_name = '饮品票'
        verbose_name_plural = '饮品票'
        ordering = ['status', 'created_at']
    
    def __str__(self):
        return self.ticket_number
