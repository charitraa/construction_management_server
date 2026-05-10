from django.db.models import Count, Sum, Q, F
from django.db.models.functions import Substr
from .models import Attendance
from employee.models import Employee


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

    @staticmethod
    def get_all_employees():
        """Get all employees."""
        return Employee.objects.all()

    @staticmethod
    def get_employees_with_attendance(date, search_term=None, department=None, status=None):
        """
        Get all employees with their attendance status for a specific date.
        Supports filtering by search term (name/email), department (role), and attendance status.
        """
        employees = Employee.objects.all()

        # Filter by search term (name or email)
        if search_term:
            employees = employees.filter(
                Q(name__icontains=search_term) |
                Q(email__icontains=search_term)
            )

        # Filter by department (role)
        if department and department != 'all':
            employees = employees.filter(role=department)

        employees_list = []
        for employee in employees:
            attendance = Attendance.objects.filter(employee=employee, date=date).first()

            employee_data = {
                'id': str(employee.id),
                'name': employee.name,
                'email': employee.email or '',
                'department': employee.role,
                'avatar': employee.avatar or '',
                'status': attendance.status if attendance else None,
                'record_id': str(attendance.id) if attendance else None,
            }

            # Filter by status if provided
            if status and status != 'all' and employee_data['status'] != status:
                continue

            employees_list.append(employee_data)

        return employees_list

    @staticmethod
    def get_unique_departments():
        """Get list of unique departments (roles) from employees."""
        return list(set(Employee.objects.values_list('role', flat=True).exclude(role__isnull=True).exclude(role='')))

    @staticmethod
    def get_total_employees_count():
        """Get total count of employees."""
        return Employee.objects.count()

    @staticmethod
    def get_stats_by_date_range(start_date, end_date):
        """
        Get attendance statistics for a date range.
        Returns detailed statistics including attendance rate.
        """
        records = Attendance.objects.filter(date__range=[start_date, end_date])
        unique_dates = records.values('date').distinct().count()
        total_records = records.count()
        present = records.filter(status='Present').count()
        absent = records.filter(status='Absent').count()
        attendance_rate = (present / total_records * 100) if total_records > 0 else 0

        return {
            'total_days': unique_dates,
            'total_records': total_records,
            'total_present': present,
            'total_absent': absent,
            'average_attendance': round(attendance_rate, 1)
        }

    @staticmethod
    def get_export_data(start_date, end_date, department=None, status=None):
        """
        Get attendance data for export with optional filters.
        Returns list of records with employee details.
        """
        records = Attendance.objects.filter(date__range=[start_date, end_date])

        # Filter by department (employee role)
        if department and department != 'all':
            records = records.filter(employee__role=department)

        # Filter by status
        if status and status != 'all':
            records = records.filter(status=status)

        export_data = []
        for record in records.select_related('employee'):
            export_data.append({
                'date': record.date.strftime('%Y-%m-%d'),
                'day': record.date.strftime('%A'),
                'employee_name': record.employee.name,
                'email': record.employee.email or '',
                'department': record.employee.role,
                'status': record.status, 
                'recorded_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
               
            })

        return export_data
