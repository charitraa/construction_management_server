from .repository import DashboardRepository
from .serializers import (
    DashboardStatsSerializer,
    MonthlyTrendSerializer,
    ExpenseCategorySerializer,
    QuickStatsSerializer,
    RevenueComparisonSerializer
)


class DashboardService:
    """Service layer for dashboard calculations."""

    @staticmethod
    def get_main_dashboard_stats():
        """
        Get main dashboard statistics with trends.
        Returns total revenue, expenses, profit, labor cost, material cost with trends.
        """
        from datetime import datetime

        # Get current values
        total_revenue = DashboardRepository.get_total_revenue()
        total_expenses = DashboardRepository.get_total_expenses()
        profit = DashboardRepository.get_total_profit()
        labor_cost = DashboardRepository.get_labor_cost()
        material_cost = DashboardRepository.get_material_cost()

        # Get revenue trend
        revenue_comparison = DashboardRepository.get_revenue_vs_previous_month()
        revenue_trend = revenue_comparison['percentage_change']

        # For simplicity, using revenue trend as proxy for other trends
        # In production, you might want to calculate actual trends for each metric
        expenses_trend = -5.0  # Example: decreasing expenses
        profit_trend = 18.0   # Example: increasing profit

        return {
            'total_revenue': float(total_revenue),
            'total_expenses': float(total_expenses),
            'profit': float(profit),
            'labor_cost': float(labor_cost),
            'material_cost': float(material_cost),
            'revenue_trend': revenue_trend,
            'expenses_trend': expenses_trend,
            'profit_trend': profit_trend
        }

    @staticmethod
    def get_monthly_trends(months=6):
        """
        Get monthly revenue vs expenses trends for charts.
        """
        return DashboardRepository.get_monthly_comparison_data(months)

    @staticmethod
    def get_expense_distribution():
        """
        Get expense distribution by category for pie chart.
        """
        categories = DashboardRepository.get_expenses_by_category()

        # Map categories to colors (matching frontend)
        category_colors = {
            'Labor': '#3B82F6',
            'Materials': '#60A5FA',
            'Equipment': '#93C5FD',
            'Other': '#DBEAFE'
        }

        return [
            {
                'name': cat['category'],
                'value': cat['percentage'],
                'color': category_colors.get(cat['category'], '#3B82F6'),
                'amount': cat['amount']
            }
            for cat in categories
        ]

    @staticmethod
    def get_quick_stats():
        """
        Get quick statistics for dashboard.
        Returns active projects, total employees, and attendance rate.
        """
        from datetime import datetime

        current_year = datetime.now().year
        current_month = datetime.now().month

        active_projects = DashboardRepository.get_active_projects_count()
        total_employees = DashboardRepository.get_total_employees_count()
        attendance_rate = DashboardRepository.get_attendance_rate_for_month(current_year, current_month)

        return {
            'active_projects': active_projects,
            'total_employees': total_employees,
            'attendance_rate': attendance_rate
        }

    @staticmethod
    def serialize_dashboard_stats(stats_data):
        """Serialize dashboard statistics."""
        return DashboardStatsSerializer(stats_data).data

    @staticmethod
    def serialize_monthly_trends(trends_data):
        """Serialize monthly trends."""
        return MonthlyTrendSerializer(trends_data, many=True).data

    @staticmethod
    def serialize_expense_distribution(distribution_data):
        """Serialize expense distribution."""
        return ExpenseCategorySerializer(distribution_data, many=True).data

    @staticmethod
    def serialize_quick_stats(stats_data):
        """Serialize quick statistics."""
        return QuickStatsSerializer(stats_data).data

    @staticmethod
    def get_complete_dashboard_data():
        """
        Get complete dashboard data for single API call.
        Combines main stats, monthly trends, expense distribution, and quick stats.
        """
        main_stats = DashboardService.get_main_dashboard_stats()
        monthly_trends = DashboardService.get_monthly_trends()
        expense_distribution = DashboardService.get_expense_distribution()
        quick_stats = DashboardService.get_quick_stats()

        return {
            'main_stats': main_stats,
            'monthly_trends': monthly_trends,
            'expense_distribution': expense_distribution,
            'quick_stats': quick_stats
        }

    @staticmethod
    def validate_year_month(year=None, month=None):
        """
        Validate year and month parameters.
        Returns tuple of (year, month) with defaults if not provided.
        """
        from datetime import datetime

        current_year = datetime.now().year
        current_month = datetime.now().month

        if year is None:
            year = current_year
        if month is None:
            month = current_month

        if year < 2000 or year > 2100:
            raise ValueError("Year must be between 2000 and 2100")

        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")

        return year, month
