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
        Get attendance statistics for a specific date.
        Returns total, present, absent, and percentage.
        """
        if not date:
            from django.utils import timezone
            date = timezone.now().date()

        stats = AttendanceRepository.get_stats_by_date(date)
        total = AttendanceRepository.get_total_employees_count()
        present = stats['present']
        absent = stats['absent']
        percentage = (present / total * 100) if total > 0 else 0

        return {
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': round(percentage, 1)
        }

    @staticmethod
    def check_attendance_exists(employee_id, date):
        """Check if attendance record already exists for employee on date."""
        return AttendanceRepository.check_exists_by_employee_and_date(employee_id, date)

    @staticmethod
    def get_employees_with_attendance(date, search_term=None, department=None, status=None):
        """
        Get all employees with their attendance status for a specific date.
        Supports filtering by search term, department, and status.
        """
        return AttendanceRepository.get_employees_with_attendance(
            date=date,
            search_term=search_term,
            department=department,
            status=status
        )

    @staticmethod
    def get_departments():
        """Get list of unique departments (roles)."""
        return list(AttendanceRepository.get_unique_departments())

    @staticmethod
    def get_date_range_summary(start_date, end_date, department=None, status=None):
        """
        Get attendance summary statistics for a date range with optional filters.
        """
        base_stats = AttendanceRepository.get_stats_by_date_range(start_date, end_date)

        # Apply filters for filtered stats
        records = AttendanceRepository.get_all()
        if start_date and end_date:
            records = records.filter(date__range=[start_date, end_date])

        if department and department != 'all':
            records = records.filter(employee__role=department)

        if status and status != 'all':
            records = records.filter(status=status)

        filtered_present = records.filter(status='Present').count()
        filtered_absent = records.filter(status='Absent').count()
        filtered_total = records.count()
        filtered_percentage = (filtered_present / filtered_total * 100) if filtered_total > 0 else 0

        return {
            'total_days': base_stats['total_days'],
            'total_records': base_stats['total_records'],
            'total_present': filtered_present,
            'total_absent': filtered_absent,
            'average_attendance': round(filtered_percentage, 1)
        }

    @staticmethod
    def get_export_data(start_date, end_date, department=None, status=None):
        """
        Get attendance data for export with optional filters.
        """
        return AttendanceRepository.get_export_data(
            start_date=start_date,
            end_date=end_date,
            department=department,
            status=status
        )
