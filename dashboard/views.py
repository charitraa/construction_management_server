from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from .services import DashboardService
from .exceptions import DashboardDataNotFoundException, DashboardCalculationException
import csv
import io


class DashboardOverviewView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get complete dashboard overview data."""
        try:
            dashboard_data = DashboardService.get_complete_dashboard_data()

            return Response({
                "data": dashboard_data,
                "message": "Dashboard overview retrieved successfully"
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise DashboardCalculationException(f"Failed to generate dashboard data: {str(e)}")


class DashboardStatsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get main dashboard statistics."""
        try:
            stats = DashboardService.get_main_dashboard_stats()

            return Response({
                "data": stats,
                "message": "Dashboard statistics retrieved successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            raise DashboardCalculationException(f"Failed to get dashboard statistics: {str(e)}")


class MonthlyTrendsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get monthly revenue vs expenses trends."""
        months = request.query_params.get('months', 6)

        try:
            months = int(months)
            if months < 1 or months > 12:
                return Response({
                    "error": "Months must be between 1 and 12"
                }, status=status.HTTP_400_BAD_REQUEST)

            trends = DashboardService.get_monthly_trends(months)

            return Response({
                "data": trends,
                "message": "Monthly trends retrieved successfully"
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({
                "error": "Invalid months parameter"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise DashboardCalculationException(f"Failed to get monthly trends: {str(e)}")


class ExpenseDistributionView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get expense distribution by category."""
        try:
            distribution = DashboardService.get_expense_distribution()

            return Response({
                "data": distribution,
                "message": "Expense distribution retrieved successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            raise DashboardCalculationException(f"Failed to get expense distribution: {str(e)}")


class QuickStatsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Get quick statistics for dashboard."""
        try:
            stats = DashboardService.get_quick_stats()

            return Response({
                "data": stats,
                "message": "Quick statistics retrieved successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            raise DashboardCalculationException(f"Failed to get quick statistics: {str(e)}")


class DashboardExportView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Export dashboard data as CSV."""
        export_type = request.query_params.get('type', 'overview')

        try:
            if export_type == 'overview':
                # Export complete dashboard data
                dashboard_data = DashboardService.get_complete_dashboard_data()
                return self._export_overview(dashboard_data)
            elif export_type == 'trends':
                # Export monthly trends
                months = int(request.query_params.get('months', 6))
                trends = DashboardService.get_monthly_trends(months)
                return self._export_trends(trends)
            elif export_type == 'expenses':
                # Export expense distribution
                distribution = DashboardService.get_expense_distribution()
                return self._export_expenses(distribution)
            else:
                return Response({
                    "error": "Invalid export type. Use 'overview', 'trends', or 'expenses'"
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise DashboardCalculationException(f"Failed to export dashboard data: {str(e)}")

    def _export_overview(self, dashboard_data):
        """Export dashboard overview as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Main Stats
        writer.writerow(['DASHBOARD OVERVIEW'])
        writer.writerow([])
        writer.writerow(['Metric', 'Value'])

        main_stats = dashboard_data.get('main_stats', {})
        writer.writerow(['Total Revenue', main_stats.get('total_revenue', 0)])
        writer.writerow(['Total Expenses', main_stats.get('total_expenses', 0)])
        writer.writerow(['Profit', main_stats.get('profit', 0)])
        writer.writerow(['Labor Cost', main_stats.get('labor_cost', 0)])
        writer.writerow(['Material Cost', main_stats.get('material_cost', 0)])

        # Quick Stats
        writer.writerow([])
        writer.writerow(['QUICK STATISTICS'])
        writer.writerow([])
        writer.writerow(['Metric', 'Value'])

        quick_stats = dashboard_data.get('quick_stats', {})
        writer.writerow(['Active Projects', quick_stats.get('active_projects', 0)])
        writer.writerow(['Total Employees', quick_stats.get('total_employees', 0)])
        writer.writerow(['Attendance Rate (%)', quick_stats.get('attendance_rate', 0)])

        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Dashboard overview exported successfully"
        }, status=status.HTTP_200_OK)

    def _export_trends(self, trends):
        """Export monthly trends as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Month', 'Revenue', 'Expenses'])

        for trend in trends:
            writer.writerow([
                trend.get('month', ''),
                trend.get('revenue', 0),
                trend.get('expenses', 0)
            ])

        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Monthly trends exported successfully"
        }, status=status.HTTP_200_OK)

    def _export_expenses(self, distribution):
        """Export expense distribution as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Category', 'Amount', 'Percentage (%)'])

        for category in distribution:
            writer.writerow([
                category.get('name', ''),
                category.get('amount', 0),
                category.get('value', 0)
            ])

        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Expense distribution exported successfully"
        }, status=status.HTTP_200_OK)
