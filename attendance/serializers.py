from rest_framework import serializers
from .models import Attendance
from employee.models import Employee


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for attendance model with employee details."""

    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_role = serializers.CharField(source='employee.role', read_only=True)
    employee_id = serializers.UUIDField(source='employee.id', read_only=True)
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    employee_avatar = serializers.CharField(source='employee.avatar', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'date', 'employee', 'employee_id', 'employee_name', 'employee_role',
            'employee_email', 'employee_avatar', 'status','created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AttendanceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating attendance records."""

    class Meta:
        model = Attendance
        fields = ['date', 'employee', 'status']

    def validate_status(self, value):
        valid_statuses = ['Full Day', 'Half Day', 'Absent']
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
        valid_statuses = ['Full Day', 'Half Day', 'Absent']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}")
        return value

    def validate_employee(self, value):
        """Validate that employee exists."""
        if not value:
            raise serializers.ValidationError("Employee is required.")
        return value


class EmployeeAttendanceSerializer(serializers.Serializer):
    """Serializer for employee attendance list response."""

    id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField(allow_blank=True, allow_null=True)
    department = serializers.CharField()
    avatar = serializers.CharField(allow_blank=True, allow_null=True)
    status = serializers.CharField(allow_null=True)
    record_id = serializers.CharField(allow_null=True)


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employee data."""

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'role', 'avatar', 'daily_rate', 'phone', 'address']
        read_only_fields = ['id']


class DepartmentSerializer(serializers.Serializer):
    """Serializer for department list."""

    name = serializers.CharField()
