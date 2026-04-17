from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'client_name', 'location',
            'start_date', 'end_date', 'status', 'budget', 'contract_value',
            'created_at', 'updated_at'
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'client_name', 'location',
            'start_date', 'end_date', 'status', 'budget', 'contract_value'
        ]

    def validate_contract_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Contract value must be greater than or equal to 0")
        return value

    def validate_budget(self, value):
        if value < 0:
            raise serializers.ValidationError("Budget must be greater than or equal to 0")
        return value

    def validate(self, data):
        """Validate end date is after start date."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after start date")

        return data


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'client_name', 'location',
            'start_date', 'end_date', 'status', 'budget', 'contract_value'
        ]

    def validate_contract_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Contract value must be greater than or equal to 0")
        return value

    def validate_budget(self, value):
        if value < 0:
            raise serializers.ValidationError("Budget must be greater than or equal to 0")
        return value

    def validate(self, data):
        """Validate end date is after start date."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after start date")

        return data