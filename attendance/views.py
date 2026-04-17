from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from .serializers import (
    AttendanceSerializer,
    AttendanceCreateSerializer,
    AttendanceUpdateSerializer
)
from .services import AttendanceService
from .exceptions import AttendanceNotFoundException
import csv
import io


class AttendanceListView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get all attendance records with optional filtering."""
        attendance = AttendanceService.get_all_attendance()

        # Filter by date
        date = request.query_params.get('date')
        if date:
            attendance = attendance.filter(date=date)

        # Filter by date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            attendance = attendance.filter(date__range=[start_date, end_date])

        # Filter by employee
        employee_id = request.query_params.get('employee_id')
        if employee_id:
            attendance = attendance.filter(employee_id=employee_id)

        # Filter by status
        status_param = request.query_params.get('status')
        if status_param:
            attendance = attendance.filter(status=status_param)

        return Response({
            "data": AttendanceService.serialize_attendance_list(attendance),
            "message": "Attendance list retrieved successfully"
        }, status=status.HTTP_200_OK)


class AttendanceCreateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, *args, **kwargs):
        """Create a new attendance record."""
        serializer = AttendanceCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            attendance = serializer.save()
            return Response({
                "data": AttendanceService.serialize_attendance(attendance),
                "message": "Attendance created successfully"
            }, status=status.HTTP_201_CREATED)


class AttendanceRetrieveView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, attendance_id, *args, **kwargs):
        """Get attendance record by ID."""
        attendance = AttendanceService.get_attendance_by_id(attendance_id)
        if not attendance:
            raise AttendanceNotFoundException("Attendance record not found.")
        return Response({
            "data": AttendanceService.serialize_attendance(attendance),
            "message": "Attendance details retrieved successfully"
        }, status=status.HTTP_200_OK)


class AttendanceUpdateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def put(self, request, attendance_id, *args, **kwargs):
        """Update attendance record."""
        attendance = AttendanceService.get_attendance_by_id(attendance_id)
        if not attendance:
            raise AttendanceNotFoundException("Attendance record not found.")
        serializer = AttendanceUpdateSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            attendance = serializer.save()
            return Response({
                "data": AttendanceService.serialize_attendance(attendance),
                "message": "Attendance updated successfully"
            }, status=status.HTTP_200_OK)


class AttendanceDestroyView(APIView):
    permission_classes = [LoginRequiredPermission]

    def delete(self, request, attendance_id, *args, **kwargs):
        """Delete attendance record."""
        attendance = AttendanceService.get_attendance_by_id(attendance_id)
        if not attendance:
            raise AttendanceNotFoundException("Attendance record not found.")
        AttendanceService.delete_attendance(attendance)
        return Response({
            "message": "Attendance deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class AttendanceByDateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get attendance records for a specific date."""
        date = request.query_params.get('date')
        if not date:
            return Response({
                "error": "Date parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        attendance = AttendanceService.get_attendance_by_date(date)
        return Response({
            "data": AttendanceService.serialize_attendance_list(attendance),
            "message": "Attendance records retrieved successfully"
        }, status=status.HTTP_200_OK)


class AttendanceStatsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get attendance statistics."""
        date = request.query_params.get('date')
        stats = AttendanceService.get_attendance_stats(date)
        return Response({
            "data": stats,
            "message": "Attendance statistics retrieved successfully"
        }, status=status.HTTP_200_OK)


class AttendanceExportView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Export attendance data as CSV with optional date range filtering."""
        attendance = AttendanceService.get_all_attendance()

        # Filter by date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            attendance = attendance.filter(date__range=[start_date, end_date])

        # Filter by date
        date = request.query_params.get('date')
        if date:
            attendance = attendance.filter(date=date)

        if not attendance.exists():
            return Response({
                "error": "No attendance records to export"
            }, status=status.HTTP_400_BAD_REQUEST)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Employee Name', 'Employee Role', 'Status'])

        for record in attendance:
            writer.writerow([
                record.date,
                record.employee.name,
                record.employee.role,
                record.status
            ])

        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Attendance data exported successfully"
        }, status=status.HTTP_200_OK)
