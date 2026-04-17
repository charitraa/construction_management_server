from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from employee.models import Employee
from attendance.models import Attendance
from advance.models import Advance


class PayrollRepository:
    """Repository for payroll data calculations and aggregation."""

    @staticmethod
    def get_all_employees():
        """Get all active employees."""
        return Employee.objects.all()

    @staticmethod
    def get_employee_by_id(employee_id):
        """Get specific employee by ID."""
        return Employee.objects.filter(id=employee_id).first()

    @staticmethod
    def get_attendance_by_employee_and_month(employee_id, year, month):
        """
        Get attendance records for a specific employee in a specific month.
        Returns only present days for payroll calculation.
        """
        return Attendance.objects.filter(
            employee_id=employee_id,
            date__year=year,
            date__month=month,
            status='Present'
        )

    @staticmethod
    def get_total_advances_by_employee(employee_id):
        """
        Get total advance amount for a specific employee.
        This is cumulative total of all advances.
        """
        result = Advance.objects.filter(employee_id=employee_id).aggregate(
            total=Sum('amount')
        )
        return result['total'] or 0

    @staticmethod
    def get_advances_by_employee_and_month(employee_id, year, month):
        """
        Get advance records for a specific employee in a specific month.
        """
        return Advance.objects.filter(
            employee_id=employee_id,
            date__year=year,
            date__month=month
        )

    @staticmethod
    def get_total_advances_by_employee_and_month(employee_id, year, month):
        """
        Get total advance amount for a specific employee in a specific month.
        """
        result = Advance.objects.filter(
            employee_id=employee_id,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))
        return result['total'] or 0

    @staticmethod
    def count_present_days_by_employee_and_month(employee_id, year, month):
        """
        Count present days for a specific employee in a specific month.
        """
        return Attendance.objects.filter(
            employee_id=employee_id,
            date__year=year,
            date__month=month,
            status='Present'
        ).count()

    @staticmethod
    def get_payroll_summary_for_month(year, month):
        """
        Get payroll summary for all employees in a specific month.
        Returns aggregated totals.
        """
        # Get total wages for the month
        total_wages = 0
        employees = PayrollRepository.get_all_employees()
        for employee in employees:
            days_worked = PayrollRepository.count_present_days_by_employee_and_month(
                employee.id, year, month
            )
            total_wages += days_worked * float(employee.daily_rate)

        # Get total advances for the month
        total_advances = Advance.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        return {
            'total_wages': total_wages,
            'total_advances': total_advances,
            'total_net_pay': total_wages - total_advances
        }
