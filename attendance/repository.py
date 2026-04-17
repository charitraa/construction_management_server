from django.db.models import Count, Sum
from .models import Attendance


class AttendanceRepository:

    @staticmethod
    def get_all():
        return Attendance.objects.all()

    @staticmethod
    def get_by_id(attendance_id):
        return Attendance.objects.filter(id=attendance_id).first()

    @staticmethod
    def get_by_date(date):
        return Attendance.objects.filter(date=date)

    @staticmethod
    def get_by_date_range(start_date, end_date):
        return Attendance.objects.filter(date__range=[start_date, end_date])

    @staticmethod
    def get_by_employee(employee_id):
        return Attendance.objects.filter(employee_id=employee_id)

    @staticmethod
    def get_by_status(status):
        return Attendance.objects.filter(status=status)

    @staticmethod
    def get_by_employee_and_date(employee_id, date):
        return Attendance.objects.filter(employee_id=employee_id, date=date).first()

    @staticmethod
    def create_attendance(attendance_data):
        return Attendance.objects.create(**attendance_data)

    @staticmethod
    def update_attendance(attendance, update_data):
        for key, value in update_data.items():
            setattr(attendance, key, value)
        attendance.save()
        return attendance

    @staticmethod
    def delete_attendance(attendance):
        attendance.delete()

    @staticmethod
    def count_all():
        return Attendance.objects.count()

    @staticmethod
    def count_by_date(date):
        return Attendance.objects.filter(date=date).count()

    @staticmethod
    def count_by_status(status):
        return Attendance.objects.filter(status=status).count()

    @staticmethod
    def get_stats_by_date(date):
        """
        Get attendance statistics for a specific date.
        Returns counts for total, present, and absent.
        """
        queryset = Attendance.objects.filter(date=date)
        total = queryset.count()
        present = queryset.filter(status='Present').count()
        absent = queryset.filter(status='Absent').count()
        return {
            'total': total,
            'present': present,
            'absent': absent
        }

    @staticmethod
    def check_exists_by_employee_and_date(employee_id, date):
        return Attendance.objects.filter(employee_id=employee_id, date=date).exists()
