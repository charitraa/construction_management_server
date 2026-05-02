from .repository import RevenueRepository
from .serializers import RevenueSerializer


class RevenueService:
    
    @staticmethod
    def get_all_revenues():
        return RevenueRepository.get_all()
    
    @staticmethod
    def get_revenue_by_id(revenue_id):
        return RevenueRepository.get_by_id(revenue_id)
    
    @staticmethod
    def get_revenues_by_status(status):
        return RevenueRepository.get_by_status(status)
    
    @staticmethod
    def get_revenues_by_pay_method(pay_method):
        return RevenueRepository.get_by_pay_method(pay_method)
    
    @staticmethod
    def get_revenues_by_date_range(start_date, end_date):
        return RevenueRepository.get_by_date_range(start_date, end_date)
    
    @staticmethod
    def create_revenue(revenue_data):
        return RevenueRepository.create_revenue(revenue_data)
    
    @staticmethod
    def update_revenue(revenue, update_data):
        return RevenueRepository.update_revenue(revenue, update_data)
    
    @staticmethod
    def delete_revenue(revenue):
        RevenueRepository.delete_revenue(revenue)
    
    @staticmethod
    def serialize_revenue(revenue):
        return RevenueSerializer(revenue).data
    
    @staticmethod
    def serialize_revenues(revenues):
        return RevenueSerializer(revenues, many=True).data
    
    @staticmethod
    def get_revenue_stats():
        return {
            "total_revenue": RevenueRepository.total_amount(),
            "average_revenue": RevenueRepository.average_amount(),
            "highest_revenue": RevenueRepository.highest_amount(),
            "total_records": RevenueRepository.count_all(),
            "project_breakdown": RevenueRepository.total_by_project(),
        }