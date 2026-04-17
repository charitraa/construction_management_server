from django.db.models import Sum, Count, Avg, F
from django.db.models.functions import ExtractMonth, ExtractYear, TruncMonth
from revenue.models import Revenue
from expense.models import Expense
from employee.models import Employee
from attendance.models import Attendance
from project.models import Project


class DashboardRepository:
    """Repository for dashboard data aggregation from multiple models."""

    @staticmethod
    def get_total_revenue():
        """Get total revenue from all time."""
        result = Revenue.objects.aggregate(total=Sum('amount'))
        return result['total'] or 0

    @staticmethod
    def get_revenue_by_month(year, month):
        """Get revenue for a specific month."""
        return Revenue.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

    @staticmethod
    def get_monthly_revenue_trends(months=6):
        """
        Get monthly revenue trends for the last N months.
        Returns list of tuples (month_name, revenue_amount).
        """
        from django.db.models.functions import TruncMonth
        from django.db.models.functions import Extract

        recent_revenue = Revenue.objects.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('-month')[:months]

        month_names = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        return [
            {
                'month': month_names[rev['month'].month],
                'revenue': float(rev['total'] or 0)
            }
            for rev in reversed(recent_revenue)
        ]

    @staticmethod
    def get_revenue_vs_previous_month():
        """
        Compare current month revenue with previous month.
        Returns current_month, previous_month, percentage_change.
        """
        from datetime import datetime

        current_month = datetime.now().month
        current_year = datetime.now().year

        current_revenue = Revenue.objects.filter(
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate previous month
        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year

        previous_revenue = Revenue.objects.filter(
            date__year=prev_year,
            date__month=prev_month
        ).aggregate(total=Sum('amount'))['total'] or 0

        if previous_revenue == 0:
            percentage_change = 100 if current_revenue > 0 else 0
        else:
            percentage_change = ((current_revenue - previous_revenue) / previous_revenue) * 100

        return {
            'current_month_revenue': current_revenue,
            'previous_month_revenue': previous_revenue,
            'percentage_change': round(percentage_change, 1)
        }

    @staticmethod
    def get_total_expenses():
        """Get total expenses from all time."""
        result = Expense.objects.aggregate(total=Sum('amount'))
        return result['total'] or 0

    @staticmethod
    def get_expenses_by_month(year, month):
        """Get expenses for a specific month."""
        return Expense.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

    @staticmethod
    def get_monthly_expense_trends(months=6):
        """
        Get monthly expense trends for the last N months.
        Returns list of tuples (month_name, expense_amount).
        """
        recent_expenses = Expense.objects.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('-month')[:months]

        month_names = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        return [
            {
                'month': month_names[exp['month'].month],
                'expenses': float(exp['total'] or 0)
            }
            for exp in reversed(recent_expenses)
        ]

    @staticmethod
    def get_expenses_by_category():
        """Get total expenses grouped by category."""
        category_totals = Expense.objects.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')

        total_expenses = sum(exp['total'] for exp in category_totals)

        return [
            {
                'category': exp['category'],
                'amount': float(exp['total']),
                'percentage': round((exp['total'] / total_expenses * 100), 1) if total_expenses > 0 else 0
            }
            for exp in category_totals
        ]

    @staticmethod
    def get_labor_cost():
        """Get total labor expenses."""
        result = Expense.objects.filter(category='Labor').aggregate(total=Sum('amount'))
        return result['total'] or 0

    @staticmethod
    def get_material_cost():
        """Get total material expenses."""
        result = Expense.objects.filter(category='Materials').aggregate(total=Sum('amount'))
        return result['total'] or 0

    @staticmethod
    def get_equipment_cost():
        """Get total equipment expenses."""
        result = Expense.objects.filter(category='Equipment').aggregate(total=Sum('amount'))
        return result['total'] or 0

    @staticmethod
    def get_other_cost():
        """Get total other expenses."""
        result = Expense.objects.filter(category='Other').aggregate(total=Sum('amount'))
        return result['total'] or 0

    @staticmethod
    def get_total_profit():
        """Calculate total profit (revenue - expenses)."""
        total_revenue = DashboardRepository.get_total_revenue()
        total_expenses = DashboardRepository.get_total_expenses()
        return total_revenue - total_expenses

    @staticmethod
    def get_profit_by_month(year, month):
        """Calculate profit for a specific month."""
        revenue = DashboardRepository.get_revenue_by_month(year, month)
        expenses = DashboardRepository.get_expenses_by_month(year, month)
        return revenue - expenses

    @staticmethod
    def get_active_projects_count():
        """Get count of active/ongoing projects."""
        return Project.objects.filter(status='ongoing').count()

    @staticmethod
    def get_total_employees_count():
        """Get total count of employees."""
        return Employee.objects.count()

    @staticmethod
    def get_attendance_rate_for_month(year, month):
        """Calculate attendance rate for a specific month."""
        total_attendance = Attendance.objects.filter(
            date__year=year,
            date__month=month
        )

        if total_attendance.count() == 0:
            return 0

        present_count = total_attendance.filter(status='Present').count()
        attendance_rate = (present_count / total_attendance.count()) * 100

        return round(attendance_rate, 1)

    @staticmethod
    def get_monthly_comparison_data(months=6):
        """
        Get monthly revenue vs expenses comparison data for charts.
        Returns list of dictionaries with month, revenue, and expenses.
        """
        from django.db.models import F

        revenue_data = DashboardRepository.get_monthly_revenue_trends(months)
        expense_data = DashboardRepository.get_monthly_expense_trends(months)

        # Combine data by month
        combined_data = {}
        for rev in revenue_data:
            combined_data[rev['month']] = {'month': rev['month'], 'revenue': rev['revenue'], 'expenses': 0}

        for exp in expense_data:
            if exp['month'] in combined_data:
                combined_data[exp['month']]['expenses'] = exp['expenses']
            else:
                combined_data[exp['month']] = {'month': exp['month'], 'revenue': 0, 'expenses': exp['expenses']}

        return list(combined_data.values())
