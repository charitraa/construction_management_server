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