from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'role', 'daily_rate', 'phone', 'created_at', 'updated_at']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'role', 'daily_rate', 'phone']

    def validate_daily_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("Daily rate must be greater than 0")
        return value


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'role', 'daily_rate', 'phone']

    def validate_daily_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("Daily rate must be greater than 0")
        return value