from django.db import models
from django.utils import timezone
from product.models import Product
from sales.models import Order, Customer

class SalesReport(models.Model):
    """销售报表模型"""
    REPORT_TYPES = [
        ('daily', '日报'),
        ('weekly', '周报'),
        ('monthly', '月报'),
    ]
    
    report_id = models.CharField(max_length=30, unique=True, verbose_name='报告ID')
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES, verbose_name='报告类型')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')
    
    class Meta:
        verbose_name = '销售报表'
        verbose_name_plural = verbose_name
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} {self.start_date} 至 {self.end_date}"

class TopSellingProduct(models.Model):
    """畅销商品排行模型"""
    report = models.ForeignKey(SalesReport, on_delete=models.CASCADE, related_name='top_products', verbose_name='关联报表')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity_sold = models.IntegerField(verbose_name='销售数量')
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='销售金额')
    rank = models.PositiveSmallIntegerField(verbose_name='排名')
    
    class Meta:
        verbose_name = '畅销商品'
        verbose_name_plural = verbose_name
        ordering = ['report', 'rank']
        unique_together = ['report', 'product']
    
    def __str__(self):
        return f"{self.report.report_id} - {self.product.name} (第{self.rank}名)"

class CustomerFlowHeatmap(models.Model):
    """客流热力图模型"""
    date = models.DateField(verbose_name='日期')
    hour = models.PositiveSmallIntegerField(verbose_name='小时', help_text='0-23表示一天中的小时')
    customer_count = models.IntegerField(default=0, verbose_name='客流量')
    sales_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='销售额')
    
    class Meta:
        verbose_name = '客流热力图'
        verbose_name_plural = verbose_name
        ordering = ['-date', 'hour']
        unique_together = ['date', 'hour']
    
    def __str__(self):
        return f"{self.date} {self.hour}:00-{self.hour+1}:00 - {self.customer_count}人"
    
    @classmethod
    def generate_for_date(cls, date=None):
        """为指定日期生成客流热力图数据"""
        if date is None:
            date = timezone.now().date()
        
        # 查询当天每小时的订单
        for hour in range(24):
            hour_start = timezone.datetime.combine(date, timezone.time(hour=hour))
            hour_end = timezone.datetime.combine(date, timezone.time(hour=hour + 1 if hour < 23 else 23, minute=59, second=59))
            
            # 获取该小时内的订单
            hour_orders = Order.objects.filter(
                order_date__range=(hour_start, hour_end)
            )
            
            # 计算客流量（订单数）和销售额
            customer_count = hour_orders.count()
            sales_amount = hour_orders.aggregate(total=models.Sum('total_amount'))['total'] or 0
            
            # 更新或创建记录
            cls.objects.update_or_create(
                date=date,
                hour=hour,
                defaults={
                    'customer_count': customer_count,
                    'sales_amount': sales_amount,
                }
            )

class MemberRepurchaseRate(models.Model):
    """会员复购率模型"""
    date = models.DateField(verbose_name='统计日期')
    period_days = models.PositiveSmallIntegerField(verbose_name='统计周期(天)')
    total_members = models.IntegerField(default=0, verbose_name='总会员数')
    repurchase_members = models.IntegerField(default=0, verbose_name='复购会员数')
    repurchase_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='复购率(%)')
    
    class Meta:
        verbose_name = '会员复购率'
        verbose_name_plural = verbose_name
        ordering = ['-date']
        unique_together = ['date', 'period_days']
    
    def __str__(self):
        return f"{self.date} {self.period_days}天 - 复购率{self.repurchase_rate}%"
    
    @classmethod
    def calculate_repurchase_rate(cls, date=None, period_days=30):
        """计算指定日期的会员复购率"""
        if date is None:
            date = timezone.now().date()
        
        # 计算开始日期
        start_date = date - timezone.timedelta(days=period_days)
        
        # 查询所有会员
        members = Customer.objects.filter(
            customer_type__in=['member', 'vip'],
            is_active=True
        )
        
        total_members = members.count()
        repurchase_members = 0
        
        if total_members > 0:
            # 查询有多少会员在该时间段内有2次或以上的购买记录
            for member in members:
                order_count = Order.objects.filter(
                    customer=member,
                    order_date__date__range=(start_date, date),
                    status='completed',
                    payment_status=True
                ).count()
                
                if order_count >= 2:
                    repurchase_members += 1
            
            # 计算复购率
            repurchase_rate = (repurchase_members / total_members) * 100
        else:
            repurchase_rate = 0
        
        # 更新或创建记录
        repurchase_record, created = cls.objects.update_or_create(
            date=date,
            period_days=period_days,
            defaults={
                'total_members': total_members,
                'repurchase_members': repurchase_members,
                'repurchase_rate': repurchase_rate,
            }
        )
        
        return repurchase_record
