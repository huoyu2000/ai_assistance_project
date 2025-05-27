from django.db import models
from django.utils import timezone

class Category(models.Model):
    """商品分类模型"""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'product_categories'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

class Product(models.Model):
    """商品模型"""
    STATUS_CHOICES = [
        ('ACTIVE', '在售'),
        ('INACTIVE', '下架'),
        ('OUT_OF_STOCK', '缺货')
    ]
    
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(Category, models.CASCADE, db_column='category_id', null=True, blank=True)
    sku = models.CharField(max_length=32, blank=True, null=True)
    unit = models.CharField(max_length=16, default='个')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        return self.category.name if self.category else ''

    @property
    def stock_status(self):
        if self.inventory_qty <= 0:
            return 'OUT_OF_STOCK'
        elif self.inventory_qty <= self.reorder_point:
            return 'LOW_STOCK'
        return 'IN_STOCK'

# 库存水平表
class InventoryLevel(models.Model):
    product = models.OneToOneField(Product, models.CASCADE, primary_key=True, db_column='product_id')
    stock_qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=16, null=True, blank=True)
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'inventory_levels'
        verbose_name = '库存水平'
        verbose_name_plural = '库存水平'

    def __str__(self):
        return f"{self.product.name} - {self.stock_qty} {self.unit}"

    @property
    def is_low_stock(self):
        if self.stock_qty is None or self.reorder_point is None:
            return False
        return self.stock_qty <= self.reorder_point

class Recipe(models.Model):
    """饮品配方模型"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='recipe', verbose_name='关联商品')
    ingredients = models.ManyToManyField(Product, through='RecipeItem', related_name='used_in_recipes', verbose_name='配料')
    preparation_steps = models.TextField(verbose_name='制作步骤')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '饮品配方'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.product.name}的配方"

class RecipeItem(models.Model):
    """配方材料项目模型"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_items', verbose_name='配方')
    ingredient = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='配料')
    quantity = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='用量')
    unit = models.CharField(max_length=20, verbose_name='单位')
    
    class Meta:
        verbose_name = '配方项目'
        verbose_name_plural = verbose_name
        unique_together = ['recipe', 'ingredient']
    
    def __str__(self):
        return f"{self.recipe.product.name} - {self.ingredient.name}: {self.quantity}{self.unit}"

class PromotionalPrice(models.Model):
    """促销价格模型"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotional_prices', verbose_name='商品')
    name = models.CharField(max_length=100, verbose_name='促销名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='促销价格')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '促销价格'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    def is_current(self):
        """检查当前促销是否有效"""
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

class TimeSlotPrice(models.Model):
    """时段价格模型"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='time_slot_prices', verbose_name='商品')
    name = models.CharField(max_length=100, verbose_name='时段名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='时段价格')
    days_of_week = models.CharField(max_length=20, help_text='例如：0,1,2,3,4,5,6，表示周日到周六', verbose_name='生效星期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '时段价格'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
