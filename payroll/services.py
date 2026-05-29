from datetime import timedelta
from django.db.models import Sum
from advance.models import Advance
from .repository import PayrollRepository
from .serializers import EmployeePayrollSerializer, PayrollSummarySerializer


class PayrollService:

    @staticmethod
    def calculate_payroll_for_month(month_str):
        try:
            year, month = map(int, month_str.split('-'))
        except (ValueError, AttributeError):
            raise ValueError("Invalid month format. Expected YYYY-MM")

        employees = PayrollRepository.get_all_employees()
        payroll_data = []

        for employee in employees:
            # Determine calculation start date
            if employee.last_paid_date:
                calculation_start_date = employee.last_paid_date + timedelta(days=1)
            else:
                from datetime import date
                calculation_start_date = date(year, month, 1)

            # Attendance records from calculation_start_date onwards
            attendance_records = PayrollRepository.get_attendance_from_date(
                employee.id, calculation_start_date
            )

            # Day-by-day wage breakdown
            daily_wages = []
            total_wage = 0
            days_worked_since_last_payment = 0

            for attendance in attendance_records:
                if attendance.status == 'Full Day':
                    daily_wage = float(employee.daily_rate)
                    total_wage += daily_wage
                    days_worked_since_last_payment += 1
                    daily_wages.append({
                        'date': attendance.date,
                        'status': attendance.status,
                        'daily_wage': daily_wage,
                    })
                elif attendance.status == 'Half Day':
                    daily_wage = float(employee.daily_rate) / 2
                    total_wage += daily_wage
                    days_worked_since_last_payment += 0.5
                    daily_wages.append({
                        'date': attendance.date,
                        'status': attendance.status,
                        'daily_wage': daily_wage,
                    })
                else:
                    daily_wages.append({
                        'date': attendance.date,
                        'status': attendance.status,
                        'daily_wage': 0,
                    })

            # Advances taken only since calculation_start_date
            advance_result = Advance.objects.filter(
                employee=employee,
                date__gte=calculation_start_date
            ).aggregate(total=Sum('amount'))
            total_advance = float(advance_result['total'] or 0)

            net_pay = total_wage - total_advance

            payroll_data.append({
                'id': str(employee.id),
                'name': employee.name,
                'role': employee.role,
                'days_worked_since_last_payment': days_worked_since_last_payment,
                'last_payment_date': str(employee.last_paid_date) if employee.last_paid_date else None,
                'calculation_start_date': str(calculation_start_date),
                'daily_rate': float(employee.daily_rate),
                'daily_breakdown': daily_wages,
                'total_wage_earned': total_wage,
                'advance': total_advance,
                'net_pay': net_pay,
            })

        return payroll_data

    @staticmethod
    def calculate_payroll_summary_for_month(month_str):
        try:
            year, month = map(int, month_str.split('-'))
        except (ValueError, AttributeError):
            raise ValueError("Invalid month format. Expected YYYY-MM")

        return PayrollRepository.get_payroll_summary_for_month(year, month)

    @staticmethod
    def serialize_employee_payroll(payroll_data):
        return EmployeePayrollSerializer(payroll_data).data

    @staticmethod
    def serialize_payroll_summary(summary_data):
        return PayrollSummarySerializer(summary_data).data

    @staticmethod
    def serialize_payroll_list(payroll_list):
        return EmployeePayrollSerializer(payroll_list, many=True).data

    @staticmethod
    def calculate_totals_from_payroll_data(payroll_data):
        return {
            'total_wages':    sum(item['total_wage_earned'] for item in payroll_data),
            'total_advances': sum(item['advance'] for item in payroll_data),
            'total_net_pay':  sum(item['net_pay'] for item in payroll_data),
        }

    @staticmethod
    def validate_month_format(month_str):
        import re
        if not month_str or not re.match(r'^\d{4}-\d{2}$', month_str):
            raise ValueError("Invalid month format. Expected YYYY-MM")
        try:
            year, month = map(int, month_str.split('-'))
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")
            if year < 2000 or year > 2100:
                raise ValueError("Year must be between 2000 and 2100")
            return year, month
        except ValueError as e:
            raise ValueError(f"Invalid month format: {e}")