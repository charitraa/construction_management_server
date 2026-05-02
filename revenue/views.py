from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from core.pagination import StandardPagination
from django.db import models
from .serializers import (
    RevenueCreateSerializer,
    RevenueUpdateSerializer
)
from .services import RevenueService
from .exceptions import RevenueNotFoundException
import csv
import io


class RevenueListView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        revenues = RevenueService.get_all_revenues()

        # Apply filters
        search = request.query_params.get('search')
        project = request.query_params.get('project')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if search:
            revenues = revenues.filter(
                models.Q(description__icontains=search) |
                models.Q(client_name__icontains=search)
            )

        if project:
            revenues = revenues.filter(project=project)

        if start_date:
            revenues = revenues.filter(date__gte=start_date)

        if end_date:
            revenues = revenues.filter(date__lte=end_date)

        # Apply pagination
        paginator = StandardPagination()
        paginated_revenues = paginator.paginate_queryset(revenues, request)
        return paginator.get_paginated_response(
            RevenueService.serialize_revenues(paginated_revenues),
            "Revenue list retrieved successfully"
        )


class RevenueCreateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, *args, **kwargs):
        serializer = RevenueCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            revenue = serializer.save()
            return Response({
                "data": RevenueService.serialize_revenue(revenue),
                "message": "Revenue created successfully"
            }, status=status.HTTP_201_CREATED)


class RevenueRetrieveView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, revenue_id, *args, **kwargs):
        revenue = RevenueService.get_revenue_by_id(revenue_id)
        if not revenue:
            raise RevenueNotFoundException("Revenue not found.")
        return Response({
            "data": RevenueService.serialize_revenue(revenue),
            "message": "Revenue details retrieved successfully"
        }, status=status.HTTP_200_OK)


class RevenueUpdateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def put(self, request, revenue_id, *args, **kwargs):
        revenue = RevenueService.get_revenue_by_id(revenue_id)
        if not revenue:
            raise RevenueNotFoundException("Revenue not found.")
        serializer = RevenueUpdateSerializer(revenue, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            revenue = serializer.save()
            return Response({
                "data": RevenueService.serialize_revenue(revenue),
                "message": "Revenue updated successfully"
            }, status=status.HTTP_200_OK)


class RevenueDestroyView(APIView):
    permission_classes = [LoginRequiredPermission]

    def delete(self, request, revenue_id, *args, **kwargs):
        revenue = RevenueService.get_revenue_by_id(revenue_id)
        if not revenue:
            raise RevenueNotFoundException("Revenue not found.")
        RevenueService.delete_revenue(revenue)
        return Response({
            "message": "Revenue deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class RevenueStatsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        stats = RevenueService.get_revenue_stats()
        return Response({
            "data": stats,
            "message": "Revenue statistics retrieved successfully"
        }, status=status.HTTP_200_OK)


class RevenueExportView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        revenues = RevenueService.get_all_revenues()

        # Apply filters
        search = request.query_params.get('search')
        project = request.query_params.get('project')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status_filter = request.query_params.get('status')
        pay_method = request.query_params.get('pay_method')

        if search:
            revenues = revenues.filter(
                models.Q(description__icontains=search) |
                models.Q(client_name__icontains=search)
            )

        if project:
            revenues = revenues.filter(project=project)

        if start_date:
            revenues = revenues.filter(date__gte=start_date)

        if end_date:
            revenues = revenues.filter(date__lte=end_date)

        if status_filter:
            revenues = revenues.filter(status=status_filter)
        if pay_method:
            revenues = revenues.filter(pay_method=pay_method)
        
        if not revenues.exists():
            return Response({
                "error": "No revenue records to export"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Project ID', 'Client', 'Description', 'Amount', 'Payment Method', 'Status'])

        for rev in revenues:
            writer.writerow([rev.date, rev.project_id, rev.client_name, rev.description or '', rev.amount, rev.pay_method, rev.status])
        
        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Revenue exported successfully"
        }, status=status.HTTP_200_OK)