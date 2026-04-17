from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for attendance model with employee details."""

    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_role = serializers.CharField(source='employee.role', read_only=True)
    employee_id = serializers.UUIDField(source='employee.id', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'date', 'employee', 'employee_id', 'employee_name', 'employee_role',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AttendanceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating attendance records."""

    class Meta:
        model = Attendance
        fields = ['date', 'employee', 'status']

    def validate_status(self, value):
        valid_statuses = ['Present', 'Absent']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}")
        return value

    def validate_employee(self, value):
        """Validate that employee exists."""
        if not value:
            raise serializers.ValidationError("Employee is required.")
        return value

    def validate(self, data):
        """Check if attendance already exists for this employee on this date."""
        from attendance.services import AttendanceService

        employee = data['employee']
        date = data['date']

        if AttendanceService.check_attendance_exists(str(employee.id), date):
            raise serializers.ValidationError(
                f"Attendance already exists for employee {employee.name} on {date}"
            )

        return data


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating attendance records."""

    class Meta:
        model = Attendance
        fields = ['date', 'employee', 'status']

    def validate_status(self, value):
        valid_statuses = ['Present', 'Absent']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}")
        return value

    def validate_employee(self, value):
        """Validate that employee exists."""
        if not value:
            raise serializers.ValidationError("Employee is required.")
        return value
