from django.db.models import Sum, Avg, Max
from .models import Advance


class AdvanceRepository:
    
    @staticmethod
    def get_all():
        return Advance.objects.all()
    
    @staticmethod
    def get_by_id(advance_id):
        return Advance.objects.filter(id=advance_id).first()
    
    @staticmethod
    def get_by_employee_id(employee_id):
        return Advance.objects.filter(employee_id=employee_id)
    
    @staticmethod
    def create_advance(advance_data):
        return Advance.objects.create(**advance_data)
    
    @staticmethod
    def delete_advance(advance):
        advance.delete()
    
    @staticmethod
    def count_all():
        return Advance.objects.count()
    
    @staticmethod
    def total_amount():
        return Advance.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    @staticmethod
    def total_by_employee():
        result = Advance.objects.values('employee_id').annotate(total=Sum('amount'))
        return {str(item['employee_id']): item['total'] or 0 for item in result}

    @staticmethod
    def unique_employees_count():
        return Advance.objects.values('employee_id').distinct().count()

    @staticmethod
    def average_advance():
        result = Advance.objects.aggregate(avg=Avg('amount'))['avg']
        return result or 0

    @staticmethod
    def highest_advance():
        result = Advance.objects.aggregate(max=Max('amount'))['max']
        return result or 0