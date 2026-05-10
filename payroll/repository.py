from django.db.models import Sum
from employee.models import Employee
from attendance.models import Attendance
from advance.models import Advance


class PayrollRepository:

    @staticmethod
    def get_all_employees():
        return Employee.objects.all()

    @staticmethod
    def get_employee_by_id(employee_id):
        return Employee.objects.filter(id=employee_id).first()

    @staticmethod
    def get_attendance_from_date(employee_id, start_date):
        return Attendance.objects.filter(
            employee_id=employee_id,
            date__gte=start_date
        ).order_by('date')

    @staticmethod
    def get_payroll_summary_for_month(year, month):
        from datetime import date, timedelta

        employees = PayrollRepository.get_all_employees()
        total_wages = 0.0
        total_advances = 0.0

        for employee in employees:
            if employee.last_paid_date:
                calc_start = employee.last_paid_date + timedelta(days=1)
            else:
                calc_start = date(year, month, 1)

            attendance_records = PayrollRepository.get_attendance_from_date(
                employee.id, calc_start
            )
            for attendance in attendance_records:
                if attendance.status == 'Present':
                    total_wages += float(employee.daily_rate)

            advance_result = Advance.objects.filter(
                employee=employee,
                date__gte=calc_start
            ).aggregate(total=Sum('amount'))
            total_advances += float(advance_result['total'] or 0)

        return {
            'total_wages': total_wages,
            'total_advances': total_advances,
            'total_net_pay': total_wages - total_advances,
        }