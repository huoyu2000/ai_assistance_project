from rest_framework import serializers
from .models import DailyRevenue, CostRecord, ProfitReport

class DailyRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRevenue
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CostRecordSerializer(serializers.ModelSerializer):
    cost_type_display = serializers.CharField(source='get_cost_type_display', read_only=True)
    
    class Meta:
        model = CostRecord
        fields = [
            'id', 'date', 'cost_type', 'cost_type_display', 'amount', 
            'description', 'reference_number', 'created_by', 'created_at'
        ]
        read_only_fields = ['created_at']

class ProfitReportSerializer(serializers.ModelSerializer):
    period_type_display = serializers.CharField(source='get_period_type_display', read_only=True)
    
    class Meta:
        model = ProfitReport
        fields = [
            'id', 'report_id', 'period_type', 'period_type_display', 
            'start_date', 'end_date', 'total_revenue', 'total_cost',
            'gross_profit', 'net_profit', 'profit_margin', 'created_at'
        ]
        read_only_fields = ['created_at', 'gross_profit', 'net_profit', 'profit_margin'] 