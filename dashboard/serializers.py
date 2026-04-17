from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    """
    Serializer for main dashboard statistics.
    """

    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=15, decimal_places=2)
    profit = serializers.DecimalField(max_digits=15, decimal_places=2)
    labor_cost = serializers.DecimalField(max_digits=15, decimal_places=2)
    material_cost = serializers.DecimalField(max_digits=15, decimal_places=2)

    # Trends
    revenue_trend = serializers.FloatField()
    expenses_trend = serializers.FloatField()
    profit_trend = serializers.FloatField()


class MonthlyTrendSerializer(serializers.Serializer):
    """
    Serializer for monthly trend data.
    """

    month = serializers.CharField()
    revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=15, decimal_places=2)


class ExpenseCategorySerializer(serializers.Serializer):
    """
    Serializer for expense category distribution.
    """

    category = serializers.CharField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    percentage = serializers.FloatField()


class QuickStatsSerializer(serializers.Serializer):
    """
    Serializer for quick statistics.
    """

    active_projects = serializers.IntegerField()
    total_employees = serializers.IntegerField()
    attendance_rate = serializers.FloatField()


class RevenueComparisonSerializer(serializers.Serializer):
    """
    Serializer for revenue comparison data.
    """

    current_month_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    previous_month_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    percentage_change = serializers.FloatField()


class DashboardRequestSerializer(serializers.Serializer):
    """
    Serializer for dashboard request parameters.
    """

    year = serializers.IntegerField(required=False, help_text="Year for filtering data")
    month = serializers.IntegerField(required=False, help_text="Month (1-12) for filtering data")
    months = serializers.IntegerField(required=False, default=6, help_text="Number of months for trends")

    def validate_month(self, value):
        """Validate month range."""
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("Month must be between 1 and 12")
        return value

    def validate_months(self, value):
        """Validate months range."""
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("Months must be between 1 and 12")
        return value
