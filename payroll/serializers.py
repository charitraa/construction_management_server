from rest_framework import serializers


class EmployeePayrollSerializer(serializers.Serializer):
    """
    Serializer for individual employee payroll data.
    This is calculated data, not stored in database.
    """

    id = serializers.UUIDField()
    name = serializers.CharField()
    role = serializers.CharField()
    days_worked = serializers.IntegerField()
    daily_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_wage = serializers.DecimalField(max_digits=15, decimal_places=2)
    advance = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_pay = serializers.DecimalField(max_digits=15, decimal_places=2)


class PayrollSummarySerializer(serializers.Serializer):
    """
    Serializer for payroll summary statistics.
    """

    total_wages = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_advances = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_net_pay = serializers.DecimalField(max_digits=15, decimal_places=2)


class PayrollRequestSerializer(serializers.Serializer):
    """
    Serializer for payroll request parameters.
    """

    month = serializers.CharField(help_text="Month in YYYY-MM format")

    def validate_month(self, value):
        """Validate month format (YYYY-MM)."""
        import re
        if not re.match(r'^\d{4}-\d{2}$', value):
            raise serializers.ValidationError("Month must be in YYYY-MM format")
        return value
