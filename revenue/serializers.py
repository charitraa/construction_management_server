from rest_framework import serializers
from .models import Revenue


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['id', 'date', 'project_id', 'client_name', 'amount', 'pay_method', 'status', 'created_at', 'updated_at']


class RevenueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['id', 'date', 'project_id', 'client_name', 'amount', 'pay_method', 'status']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value


class RevenueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['date', 'project_id', 'client_name', 'amount', 'pay_method', 'status']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value