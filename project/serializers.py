from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'client_name', 'location', 'contract_value', 'created_at', 'updated_at']


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'client_name', 'location', 'contract_value']

    def validate_contract_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Contract value must be greater than 0")
        return value


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'client_name', 'location', 'contract_value']

    def validate_contract_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Contract value must be greater than 0")
        return value