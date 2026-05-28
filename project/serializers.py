from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'client_name', 'location',
            'start_date', 'status', 'budget',
            'created_at', 'updated_at'
        ]


class ProjectReceivableSerializer(serializers.ModelSerializer):
    """Per-project receivable: how much the client still owes.

    `received` is annotated on the queryset (sum of 'Received' revenue);
    `remaining` is budget minus received.
    """
    budget = serializers.FloatField()
    received = serializers.FloatField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'client_name', 'location', 'status',
            'budget', 'received', 'remaining'
        ]

    def get_remaining(self, obj):
        budget = float(obj.budget or 0)
        received = float(getattr(obj, 'received', 0) or 0)
        return round(budget - received, 2)


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'client_name', 'location',
            'start_date', 'status', 'budget'
        ]

    def validate_budget(self, value):
        if value < 0:
            raise serializers.ValidationError("Budget must be greater than or equal to 0")
        return value

    def validate(self, data):
        return data


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'client_name', 'location',
            'start_date', 'status', 'budget'
        ]

    def validate_budget(self, value):
        if value < 0:
            raise serializers.ValidationError("Budget must be greater than or equal to 0")
        return value

    def validate(self, data):
        return data