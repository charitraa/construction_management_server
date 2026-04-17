from .repository import AttendanceRepository
from .serializers import AttendanceSerializer


class AttendanceService:

    @staticmethod
    def get_all_attendance():
        return AttendanceRepository.get_all()

    @staticmethod
    def get_attendance_by_id(attendance_id):
        return AttendanceRepository.get_by_id(attendance_id)

    @staticmethod
    def get_attendance_by_date(date):
        return AttendanceRepository.get_by_date(date)

    @staticmethod
    def get_attendance_by_date_range(start_date, end_date):
        return AttendanceRepository.get_by_date_range(start_date, end_date)

    @staticmethod
    def get_attendance_by_employee(employee_id):
        return AttendanceRepository.get_by_employee(employee_id)

    @staticmethod
    def get_attendance_by_status(status):
        return AttendanceRepository.get_by_status(status)

    @staticmethod
    def get_attendance_by_employee_and_date(employee_id, date):
        return AttendanceRepository.get_by_employee_and_date(employee_id, date)

    @staticmethod
    def create_attendance(attendance_data):
        return AttendanceRepository.create_attendance(attendance_data)

    @staticmethod
    def update_attendance(attendance, update_data):
        return AttendanceRepository.update_attendance(attendance, update_data)

    @staticmethod
    def delete_attendance(attendance):
        AttendanceRepository.delete_attendance(attendance)

    @staticmethod
    def serialize_attendance(attendance):
        return AttendanceSerializer(attendance).data

    @staticmethod
    def serialize_attendance_list(attendance_list):
        return AttendanceSerializer(attendance_list, many=True).data

    @staticmethod
    def get_attendance_stats(date=None):
        """
        Get attendance statistics.
        If date is provided, get stats for that date.
        Otherwise, get overall stats.
        """
        if date:
            return AttendanceRepository.get_stats_by_date(date)

        total = AttendanceRepository.count_all()
        present = AttendanceRepository.count_by_status('Present')
        absent = AttendanceRepository.count_by_status('Absent')
        return {
            'total': total,
            'present': present,
            'absent': absent
        }

    @staticmethod
    def check_attendance_exists(employee_id, date):
        """Check if attendance record already exists for employee on date."""
        return AttendanceRepository.check_exists_by_employee_and_date(employee_id, date)
