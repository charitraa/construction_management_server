from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from core.pagination import StandardPagination
from .serializers import (
    AttendanceCreateSerializer,
    AttendanceUpdateSerializer,
    EmployeeAttendanceSerializer,
    DepartmentSerializer
)
from .services import AttendanceService
from .exceptions import AttendanceNotFoundException
import csv
import json
from django.http import HttpResponse
from django.utils import timezone


class AttendanceListView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get all attendance records with optional filtering and pagination."""
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

        # Filter by department (employee role)
        department = request.query_params.get('department')
        if department and department != 'all':
            attendance = attendance.filter(employee__role=department)

        # Apply pagination
        paginator = StandardPagination()
        paginated_attendance = paginator.paginate_queryset(attendance, request)

        return Response({
            "data": AttendanceService.serialize_attendance_list(paginated_attendance),
            "pagination": {
                "total": paginator.page.paginator.count,
                "page": paginator.page.number,
                "page_size": paginator.get_page_size(request),
                "total_pages": paginator.page.paginator.num_pages,
                "has_next": paginator.get_next_link() is not None,
                "has_previous": paginator.get_previous_link() is not None,
            },
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
        """Get attendance statistics for a specific date."""
        date = request.query_params.get('date')
        stats = AttendanceService.get_attendance_stats(date)
        return Response({
            "data": stats,
            "message": "Attendance statistics retrieved successfully"
        }, status=status.HTTP_200_OK)


class AttendanceEmployeesView(APIView):
    """
    Get all employees with their attendance status for a specific date.
    This is the main endpoint for the attendance management interface.
    """
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get employees with attendance for a specific date with filters."""
        date = request.query_params.get('date')
        if not date:
            from django.utils import timezone
            date = timezone.now().date().strftime('%Y-%m-%d')

        # Get query parameters for filtering
        search = request.query_params.get('search', '')
        department = request.query_params.get('department', 'all')
        status_filter = request.query_params.get('status', 'all')

        # Get employees with attendance
        employees_attendance = AttendanceService.get_employees_with_attendance(
            date=date,
            search_term=search,
            department=department,
            status=status_filter
        )

        # Serialize the data
        serializer = EmployeeAttendanceSerializer(employees_attendance, many=True)

        return Response({
            "data": serializer.data,
            "message": "Employees with attendance retrieved successfully"
        }, status=status.HTTP_200_OK)


class AttendanceDepartmentsView(APIView):
    """Get list of unique departments (roles)."""
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get all unique departments."""
        departments = AttendanceService.get_departments()

        # Format as list of department names
        department_list = [{'name': dept} for dept in departments]

        serializer = DepartmentSerializer(department_list, many=True)

        return Response({
            "data": ['all'] + [dept for dept in departments],
            "message": "Departments retrieved successfully"
        }, status=status.HTTP_200_OK)


class AttendanceExportView2(APIView):
    """Export attendance data as CSV or JSON with optional date range and filters."""
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Export attendance data."""
        # Get export parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        export_format = request.query_params.get('export_format', 'csv').lower()
        include_stats = request.query_params.get('include_stats', 'true').lower() == 'true'
        department = request.query_params.get('department', 'all')
        status_filter = request.query_params.get('status', 'all')

        # Validate required parameters
        if not start_date or not end_date:
            return Response({
                "error": "start_date and end_date parameters are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get export data
        export_data = AttendanceService.get_export_data(
            start_date=start_date,
            end_date=end_date,
            department=department,
            status=status_filter
        )

        if not export_data:
            return Response({
                "error": "No attendance records to export for the selected filters"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get summary statistics
        date_range_summary = AttendanceService.get_date_range_summary(
            start_date=start_date,
            end_date=end_date,
            department=department,
            status=status_filter
        )

        # Prepare summary for export
        summary = {
            'Export Date Range': f"{start_date} to {end_date}",
            'Total Days': date_range_summary['total_days'],
            'Total Records': len(export_data),
            'Present Count': date_range_summary['total_present'],
            'Absent Count': date_range_summary['total_absent'],
            'Attendance Rate': f"{date_range_summary['average_attendance']}%",
            'Department Filter': 'All Departments' if department == 'all' else department,
            'Status Filter': 'All Status' if status_filter == 'all' else status_filter,
            'Export Date': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        if export_format == 'csv':
            # Export as CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="attendance_{start_date}_to_{end_date}.csv"'

            writer = csv.writer(response)

            if include_stats:
                writer.writerow(['# ATTENDANCE SUMMARY REPORT'])
                writer.writerow(['# ' + '=' * 50])
                for key, value in summary.items():
                    writer.writerow([f'# {key}:', value])
                writer.writerow(['# ' + '=' * 50])
                writer.writerow([])

            # Write headers
            if export_data:
                headers = list(export_data[0].keys())
                writer.writerow(headers)

                # Write data rows
                for row in export_data:
                    values = [row[header] for header in headers]
                    writer.writerow(values)

            return response

        elif export_format == 'json':
            # Export as JSON
            export_output = {
                "metadata": {
                    "exportDate": timezone.now().isoformat(),
                    "dateRange": {"start": start_date, "end": end_date},
                    "filters": {
                        "department": None if department == 'all' else department,
                        "status": None if status_filter == 'all' else status_filter,
                    },
                    "summary": summary if include_stats else None,
                },
                "data": export_data,
            }

            response = HttpResponse(
                json.dumps(export_output, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="attendance_{start_date}_to_{end_date}.json"'
            return response

        else:
            return Response({
                "error": "Invalid format. Use 'csv' or 'json'"
            }, status=status.HTTP_400_BAD_REQUEST)


class AttendanceDateRangeSummaryView(APIView):
    """Get attendance summary for a date range with filters."""
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get attendance statistics for a date range."""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        department = request.query_params.get('department', 'all')
        status_filter = request.query_params.get('status', 'all')

        if not start_date or not end_date:
            return Response({
                "error": "start_date and end_date parameters are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        summary = AttendanceService.get_date_range_summary(
            start_date=start_date,
            end_date=end_date,
            department=department,
            status=status_filter
        )

        return Response({
            "data": summary,
            "message": "Date range summary retrieved successfully"
        }, status=status.HTTP_200_OK)
