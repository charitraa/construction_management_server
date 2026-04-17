from .repository import ExpenseRepository
from .serializers import ExpenseSerializer


class ExpenseService:
    
    @staticmethod
    def get_all_expenses():
        return ExpenseRepository.get_all()
    
    @staticmethod
    def get_expense_by_id(expense_id):
        return ExpenseRepository.get_by_id(expense_id)
    
    @staticmethod
    def get_expenses_by_category(category):
        return ExpenseRepository.get_by_category(category)
    
    @staticmethod
    def get_expenses_by_date_range(start_date, end_date):
        return ExpenseRepository.get_by_date_range(start_date, end_date)
    
    @staticmethod
    def create_expense(expense_data):
        return ExpenseRepository.create_expense(expense_data)
    
    @staticmethod
    def update_expense(expense, update_data):
        return ExpenseRepository.update_expense(expense, update_data)
    
    @staticmethod
    def delete_expense(expense):
        ExpenseRepository.delete_expense(expense)
    
    @staticmethod
    def serialize_expense(expense):
        return ExpenseSerializer(expense).data
    
    @staticmethod
    def serialize_expenses(expenses):
        return ExpenseSerializer(expenses, many=True).data
    
    @staticmethod
    def get_expense_stats():
        category_totals = ExpenseRepository.total_by_category()
        return {
            "total": ExpenseRepository.total_amount(),
            "total_count": ExpenseRepository.count_all(),
            "Materials": category_totals.get('Materials', 0),
            "Labor": category_totals.get('Labor', 0),
            "Equipment": category_totals.get('Equipment', 0),
            "Other": category_totals.get('Other', 0),
        }