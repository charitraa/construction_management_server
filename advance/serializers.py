from rest_framework import serializers
from .models import Advance


class AdvanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_role = serializers.CharField(source='employee.role', read_only=True)

    class Meta:
        model = Advance
        fields = ['id', 'date', 'employee', 'employee_name', 'employee_role', 'amount', 'created_at', 'updated_at']


class AdvanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance
        fields = ['id', 'date', 'employee', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate_employee(self, value):
        """Validate that employee exists."""
        if not value:
            raise serializers.ValidationError("Employee is required.")
        return value