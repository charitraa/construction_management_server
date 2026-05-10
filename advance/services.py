from .repository import AdvanceRepository
from .serializers import AdvanceSerializer


class AdvanceService:

    @staticmethod
    def get_all_advances():
        return AdvanceRepository.get_all()

    @staticmethod
    def get_advance_by_id(advance_id):
        return AdvanceRepository.get_by_id(advance_id)

    @staticmethod
    def get_advances_by_employee_id(employee_id):
        return AdvanceRepository.get_by_employee_id(employee_id)

    @staticmethod
    def create_advance(advance_data):
        return AdvanceRepository.create_advance(advance_data)

    @staticmethod
    def delete_advance(advance):
        AdvanceRepository.delete_advance(advance)

    @staticmethod
    def serialize_advance(advance):
        return AdvanceSerializer(advance).data

    @staticmethod
    def serialize_advances(advances):
        return AdvanceSerializer(advances, many=True).data

    @staticmethod
    def get_advance_stats():
        return {
            "total_advance": AdvanceRepository.total_amount(),
            "total_count": AdvanceRepository.count_all(),
            "unique_employees": AdvanceRepository.unique_employees_count(),
            "average_advance": AdvanceRepository.average_advance(),
            "highest_advance": AdvanceRepository.highest_advance(),
        }