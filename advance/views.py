from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from core.pagination import StandardPagination
from .serializers import (
    AdvanceSerializer,
    AdvanceCreateSerializer,
    AdvanceUpdateSerializer
)
from .services import AdvanceService
from .exceptions import AdvanceNotFoundException


class AdvanceListView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        advances = AdvanceService.get_all_advances()

        # Filter by search term (employee name)
        search = request.query_params.get('search')
        if search:
            advances = advances.filter(employee__name__icontains=search)

        # Filter by employee
        employee_id = request.query_params.get('employee_id')
        if employee_id:
            advances = advances.filter(employee_id=employee_id)

        # Filter by date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            advances = advances.filter(date__range=[start_date, end_date])
        elif start_date:
            advances = advances.filter(date__gte=start_date)
        elif end_date:
            advances = advances.filter(date__lte=end_date)

        # Filter by year
        year = request.query_params.get('year')
        if year:
            advances = advances.filter(date__year=year)

        # Filter by month
        month = request.query_params.get('month')
        if month:
            advances = advances.filter(date__month=month)

        # Apply pagination
        paginator = StandardPagination()
        paginated_advances = paginator.paginate_queryset(advances, request)
        return paginator.get_paginated_response(
            AdvanceService.serialize_advances(paginated_advances),
            "Advance list retrieved successfully"
        )


class AdvanceCreateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, *args, **kwargs):
        serializer = AdvanceCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            advance = serializer.save()
            return Response({
                "data": AdvanceService.serialize_advance(advance),
                "message": "Advance created successfully"
            }, status=status.HTTP_201_CREATED)


class AdvanceRetrieveView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, advance_id, *args, **kwargs):
        advance = AdvanceService.get_advance_by_id(advance_id)
        if not advance:
            raise AdvanceNotFoundException("Advance not found.")
        return Response({
            "data": AdvanceService.serialize_advance(advance),
            "message": "Advance details retrieved successfully"
        }, status=status.HTTP_200_OK)


class AdvanceUpdateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def put(self, request, advance_id, *args, **kwargs):
        advance = AdvanceService.get_advance_by_id(advance_id)
        if not advance:
            raise AdvanceNotFoundException("Advance not found.")
        serializer = AdvanceUpdateSerializer(advance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            advance = serializer.save()
            return Response({
                "data": AdvanceService.serialize_advance(advance),
                "message": "Advance updated successfully"
            }, status=status.HTTP_200_OK)


class AdvanceDestroyView(APIView):
    permission_classes = [LoginRequiredPermission]

    def delete(self, request, advance_id, *args, **kwargs):
        advance = AdvanceService.get_advance_by_id(advance_id)
        if not advance:
            raise AdvanceNotFoundException("Advance not found.")
        AdvanceService.delete_advance(advance)
        return Response({
            "message": "Advance deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class AdvanceStatsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        stats = AdvanceService.get_advance_stats()
        return Response({
            "data": stats,
            "message": "Advance statistics retrieved successfully"
        }, status=status.HTTP_200_OK)