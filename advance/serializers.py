from rest_framework import serializers
from .models import Advance


class AdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance
        fields = ['id', 'date', 'employee_id', 'amount', 'created_at', 'updated_at']


class AdvanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance
        fields = ['id', 'date', 'employee_id', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value