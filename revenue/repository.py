from django.db.models import Sum
from .models import Revenue


class RevenueRepository:
    
    @staticmethod
    def get_all():
        return Revenue.objects.all()
    
    @staticmethod
    def get_by_id(revenue_id):
        return Revenue.objects.filter(id=revenue_id).first()
    
    @staticmethod
    def get_by_status(status):
        return Revenue.objects.filter(status=status)
    
    @staticmethod
    def get_by_pay_method(pay_method):
        return Revenue.objects.filter(pay_method=pay_method)
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        return Revenue.objects.filter(date__range=[start_date, end_date])
    
    @staticmethod
    def create_revenue(revenue_data):
        return Revenue.objects.create(**revenue_data)
    
    @staticmethod
    def update_revenue(revenue, update_data):
        for key, value in update_data.items():
            setattr(revenue, key, value)
        revenue.save()
        return revenue
    
    @staticmethod
    def delete_revenue(revenue):
        revenue.delete()
    
    @staticmethod
    def count_all():
        return Revenue.objects.count()
    
    @staticmethod
    def total_amount():
        return Revenue.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    @staticmethod
    def total_by_status():
        result = Revenue.objects.values('status').annotate(total=Sum('amount'))
        return {item['status']: item['total'] or 0 for item in result}