from django.db.models import Sum
from .models import Expense


class ExpenseRepository:
    
    @staticmethod
    def get_all():
        return Expense.objects.all()
    
    @staticmethod
    def get_by_id(expense_id):
        return Expense.objects.filter(id=expense_id).first()
    
    @staticmethod
    def get_by_category(category):
        return Expense.objects.filter(category=category)
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        return Expense.objects.filter(date__range=[start_date, end_date])
    
    @staticmethod
    def create_expense(expense_data):
        return Expense.objects.create(**expense_data)
    
    @staticmethod
    def update_expense(expense, update_data):
        for key, value in update_data.items():
            setattr(expense, key, value)
        expense.save()
        return expense
    
    @staticmethod
    def delete_expense(expense):
        expense.delete()
    
    @staticmethod
    def count_all():
        return Expense.objects.count()
    
    @staticmethod
    def total_amount():
        return Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    @staticmethod
    def total_by_category():
        result = Expense.objects.values('category').annotate(total=Sum('amount'))
        return {item['category']: item['total'] or 0 for item in result}