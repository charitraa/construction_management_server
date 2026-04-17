from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'date', 'project', 'project_name', 'category', 'description', 'amount', 'created_at', 'updated_at']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'date', 'project', 'category', 'description', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate_project(self, value):
        """Validate that project exists if provided."""
        if value and not value.name:
            raise serializers.ValidationError("Project not found.")
        return value


class ExpenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['date', 'project', 'category', 'description', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate_project(self, value):
        """Validate that project exists if provided."""
        if value and not value.name:
            raise serializers.ValidationError("Project not found.")
        return value