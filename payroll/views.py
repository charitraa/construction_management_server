from datetime import date, timedelta
from employee.models import Employee
from expense.models import Expense
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from .services import PayrollService
from .exceptions import PayrollCalculationException
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

            # Write summary header
            writer.writerow(['PAYROLL SUMMARY FOR ' + month.upper()])
            writer.writerow([])

            # Write employee summaries
            writer.writerow(['Employee Name', 'Role', 'Days Since Last Payment', 'Last Payment Date', 'Calculation Start', 'Daily Rate', 'Total Wage Earned', 'Advance', 'Net Pay'])

            for record in payroll_data:
                writer.writerow([
                    record['name'],
                    record['role'],
                    record['days_worked_since_last_payment'],
                    record['last_payment_date'] or 'Never',
                    record['calculation_start_date'],
                    record['daily_rate'],
                    record['total_wage_earned'],
                    record['advance'],
                    record['net_pay']
                ])

                # Write daily breakdown for this employee
                writer.writerow([])  # Empty row for separation
                writer.writerow([f"Daily Breakdown for {record['name']}:"])
                writer.writerow(['Date', 'Status', 'Daily Wage'])

                for daily in record['daily_breakdown']:
                    writer.writerow([
                       str(daily['date']),
                        daily['status'],
                        daily['daily_wage']
                    ])

                writer.writerow([])  # Empty row after each employee's breakdown

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

class PayrollMarkAsPaidView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, *args, **kwargs):

        employee_id = request.data.get('employee_id')
        amount      = request.data.get('amount')
        days_paid   = request.data.get('days_paid')
        start_date  = request.data.get('start_date')
        end_date    = request.data.get('end_date')

        if not all([employee_id, amount, days_paid, start_date, end_date]):
            return Response(
                {"error": "employee_id, amount, days_paid, start_date, end_date are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = Employee.objects.filter(id=employee_id).first()
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()

        # Reset the calculation period — next run starts from tomorrow
        employee.last_paid_date = today
        employee.save(update_fields=['last_paid_date'])

        # Log as expense
        Expense.objects.create(
            date=today,
            category='Payment',
            description=f"Wage payment to {employee.name} ({employee.role}) — {days_paid} days ({start_date} to {end_date})",
            amount=amount
        )

        return Response({
            "data": {
                "employee_id":   str(employee.id),
                "employee_name": employee.name,
                "amount":        amount,
                "days_paid":     days_paid,
                "paid_on":       str(today),
                "next_calculation_from": str(today + timedelta(days=1)),
            },
            "message": f"Payment recorded. Next payroll for {employee.name} starts from {today + timedelta(days=1)}."
        }, status=status.HTTP_200_OK)