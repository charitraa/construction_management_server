from rest_framework import serializers
from .models import Revenue


class RevenueSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Revenue
        fields = ['id', 'date', 'project', 'project_name', 'client_name', 'amount', 'pay_method', 'status', 'created_at', 'updated_at']


class RevenueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['id', 'date', 'project', 'client_name', 'amount', 'pay_method', 'status']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate_project(self, value):
        """Validate that project exists if provided."""
        if value and not value.name:
            raise serializers.ValidationError("Project not found.")
        return value


class RevenueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['date', 'project', 'client_name', 'amount', 'pay_method', 'status']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate_project(self, value):
        """Validate that project exists if provided."""
        if value and not value.name:
            raise serializers.ValidationError("Project not found.")
        return value