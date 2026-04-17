from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from .services import PayrollService
from .exceptions import InvalidMonthException, PayrollCalculationException
from .serializers import PayrollRequestSerializer
import csv
import io


class PayrollByMonthView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get payroll data for a specific month."""
        month = request.query_params.get('month')

        if not month:
            return Response({
                "error": "Month parameter is required (YYYY-MM format)"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            PayrollService.validate_month_format(month)
            payroll_data = PayrollService.calculate_payroll_for_month(month)

            return Response({
                "data": PayrollService.serialize_payroll_list(payroll_data),
                "message": "Payroll data retrieved successfully"
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise PayrollCalculationException(f"Failed to calculate payroll: {str(e)}")


class PayrollSummaryView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get payroll summary statistics for a specific month."""
        month = request.query_params.get('month')

        if not month:
            return Response({
                "error": "Month parameter is required (YYYY-MM format)"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            PayrollService.validate_month_format(month)
            summary = PayrollService.calculate_payroll_summary_for_month(month)

            return Response({
                "data": PayrollService.serialize_payroll_summary(summary),
                "message": "Payroll summary retrieved successfully"
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise PayrollCalculationException(f"Failed to calculate payroll summary: {str(e)}")


class PayrollExportView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Export payroll data as CSV for a specific month."""
        month = request.query_params.get('month')

        if not month:
            return Response({
                "error": "Month parameter is required (YYYY-MM format)"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            PayrollService.validate_month_format(month)
            payroll_data = PayrollService.calculate_payroll_for_month(month)

            if not payroll_data:
                return Response({
                    "error": "No payroll data available for the selected month"
                }, status=status.HTTP_400_BAD_REQUEST)

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Employee Name', 'Role', 'Days Worked', 'Daily Rate', 'Total Wage', 'Advance', 'Net Pay'])

            for record in payroll_data:
                writer.writerow([
                    record['name'],
                    record['role'],
                    record['days_worked'],
                    record['daily_rate'],
                    record['total_wage'],
                    record['advance'],
                    record['net_pay']
                ])

            output.seek(0)
            return Response({
                "data": output.getvalue(),
                "message": "Payroll data exported successfully"
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise PayrollCalculationException(f"Failed to export payroll: {str(e)}")
