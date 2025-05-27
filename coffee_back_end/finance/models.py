from django.db import models
from django.utils import timezone
from sales.models import Order

class DailyRevenue(models.Model):
    """每日营业额模型"""
    date = models.DateField(unique=True, verbose_name='日期')
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='总销售额')
    total_orders = models.IntegerField(default=0, verbose_name='订单总数')
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='平均订单金额')
    cash_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='现金金额')
    wechat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='微信金额')
    alipay_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='支付宝金额')
    card_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='银行卡金额')
    member_card_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='会员卡金额')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '每日营业额'
        verbose_name_plural = verbose_name
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} - ¥{self.total_sales}"
    
    @classmethod
    def calculate_for_date(cls, date=None):
        """计算指定日期的营业额"""
        if date is None:
            date = timezone.now().date()
        
        # 查询当天所有已完成且已支付的订单
        today_orders = Order.objects.filter(
            created_at__date=date,
            status='PAID'  # 使用PAID替代completed，因为Order模型使用PAID表示已支付
        )
        
        # 计算总销售额和订单数
        total_sales = today_orders.aggregate(total=models.Sum('total'))['total'] or 0
        total_orders = today_orders.count()
        
        # 计算平均订单金额
        average_order_value = total_sales / total_orders if total_orders > 0 else 0
        
        # 注释掉按支付方式统计金额的部分，因为实际数据库表中不存在payment_method字段
        # payment_stats = {}
        # for payment_method, _ in Order.PAYMENT_METHODS:
        #     payment_stats[payment_method] = today_orders.filter(
        #         payment_method=payment_method
        #     ).aggregate(amount=models.Sum('total'))['amount'] or 0
        
        # 使用默认值替代
        payment_stats = {
            'cash': 0,
            'wechat': 0,
            'alipay': 0,
            'card': 0,
            'member_card': 0
        }
        
        # 更新或创建每日营业额记录
        daily_revenue, created = cls.objects.update_or_create(
            date=date,
            defaults={
                'total_sales': total_sales,
                'total_orders': total_orders,
                'average_order_value': average_order_value,
                'cash_amount': payment_stats.get('cash', 0),
                'wechat_amount': payment_stats.get('wechat', 0),
                'alipay_amount': payment_stats.get('alipay', 0),
                'card_amount': payment_stats.get('card', 0),
                'member_card_amount': payment_stats.get('member_card', 0),
            }
        )
        
        return daily_revenue

class CostRecord(models.Model):
    """成本记录模型"""
    COST_TYPES = [
        ('ingredients', '原料成本'),
        ('labor', '人工成本'),
        ('rent', '租金'),
        ('utilities', '水电费'),
        ('marketing', '营销费用'),
        ('maintenance', '设备维护'),
        ('misc', '其他费用'),
    ]
    
    date = models.DateField(verbose_name='日期')
    cost_type = models.CharField(max_length=15, choices=COST_TYPES, verbose_name='成本类型')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    description = models.CharField(max_length=200, verbose_name='描述')
    reference_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='参考单号')
    created_by = models.CharField(max_length=50, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '成本记录'
        verbose_name_plural = verbose_name
        ordering = ['-date', 'cost_type']
    
    def __str__(self):
        return f"{self.date} - {self.get_cost_type_display()} - ¥{self.amount}"

class ProfitReport(models.Model):
    """利润报告模型"""
    REPORT_PERIODS = [
        ('daily', '日报'),
        ('weekly', '周报'),
        ('monthly', '月报'),
        ('quarterly', '季报'),
        ('yearly', '年报'),
    ]
    
    report_id = models.CharField(max_length=30, unique=True, verbose_name='报告ID')
    period_type = models.CharField(max_length=10, choices=REPORT_PERIODS, verbose_name='报告周期')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='总收入')
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='总成本')
    gross_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='毛利润')
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='净利润')
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='利润率(%)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '利润报告'
        verbose_name_plural = verbose_name
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.get_period_type_display()} {self.start_date} 至 {self.end_date}"
    
    def calculate_profit(self):
        """计算利润"""
        # 计算总收入
        daily_revenues = DailyRevenue.objects.filter(date__range=(self.start_date, self.end_date))
        self.total_revenue = daily_revenues.aggregate(total=models.Sum('total_sales'))['total'] or 0
        
        # 计算总成本
        cost_records = CostRecord.objects.filter(date__range=(self.start_date, self.end_date))
        self.total_cost = cost_records.aggregate(total=models.Sum('amount'))['total'] or 0
        
        # 计算毛利润和净利润
        self.gross_profit = self.total_revenue - self.total_cost
        self.net_profit = self.gross_profit  # 简化模型，这里不考虑税费等
        
        # 计算利润率
        self.profit_margin = (self.net_profit / self.total_revenue * 100) if self.total_revenue > 0 else 0
        
        self.save()
        return self
