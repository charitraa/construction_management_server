from .repository import PayrollRepository
from .serializers import EmployeePayrollSerializer, PayrollSummarySerializer


class PayrollService:
    """Service layer for payroll calculations."""

    @staticmethod
    def calculate_payroll_for_month(month_str):
        """
        Calculate payroll for all employees for a specific month.

        Args:
            month_str: Month in YYYY-MM format

        Returns:
            List of payroll data for each employee
        """
        # Parse month
        try:
            year, month = map(int, month_str.split('-'))
        except (ValueError, AttributeError):
            raise ValueError("Invalid month format. Expected YYYY-MM")

        employees = PayrollRepository.get_all_employees()
        payroll_data = []

        for employee in employees:
            # Count days worked (present days)
            days_worked = PayrollRepository.count_present_days_by_employee_and_month(
                employee.id, year, month
            )

            # Calculate total wage
            total_wage = days_worked * float(employee.daily_rate)

            # Get total advance (cumulative)
            total_advance = PayrollRepository.get_total_advances_by_employee(employee.id)

            # Calculate net pay
            net_pay = total_wage - total_advance

            payroll_data.append({
                'id': str(employee.id),
                'name': employee.name,
                'role': employee.role,
                'days_worked': days_worked,
                'daily_rate': float(employee.daily_rate),
                'total_wage': total_wage,
                'advance': total_advance,
                'net_pay': net_pay
            })

        return payroll_data

    @staticmethod
    def calculate_payroll_summary_for_month(month_str):
        """
        Calculate payroll summary for a specific month.

        Args:
            month_str: Month in YYYY-MM format

        Returns:
            Summary statistics
        """
        try:
            year, month = map(int, month_str.split('-'))
        except (ValueError, AttributeError):
            raise ValueError("Invalid month format. Expected YYYY-MM")

        return PayrollRepository.get_payroll_summary_for_month(year, month)

    @staticmethod
    def serialize_employee_payroll(payroll_data):
        """Serialize employee payroll data."""
        return EmployeePayrollSerializer(payroll_data).data

    @staticmethod
    def serialize_payroll_summary(summary_data):
        """Serialize payroll summary data."""
        return PayrollSummarySerializer(summary_data).data

    @staticmethod
    def serialize_payroll_list(payroll_list):
        """Serialize list of payroll data."""
        return EmployeePayrollSerializer(payroll_list, many=True).data

    @staticmethod
    def calculate_totals_from_payroll_data(payroll_data):
        """
        Calculate totals from payroll data.

        Args:
            payroll_data: List of payroll dictionaries

        Returns:
            Dictionary with total_wages, total_advances, total_net_pay
        """
        total_wages = sum(item['total_wage'] for item in payroll_data)
        total_advances = sum(item['advance'] for item in payroll_data)
        total_net_pay = sum(item['net_pay'] for item in payroll_data)

        return {
            'total_wages': total_wages,
            'total_advances': total_advances,
            'total_net_pay': total_net_pay
        }

    @staticmethod
    def validate_month_format(month_str):
        """
        Validate month format.

        Args:
            month_str: Month string to validate

        Returns:
            Tuple of (year, month) or raises ValueError
        """
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
