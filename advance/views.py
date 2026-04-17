from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from .serializers import (
    AdvanceSerializer,
    AdvanceCreateSerializer
)
from .services import AdvanceService
from .exceptions import AdvanceNotFoundException


class AdvanceListView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        advances = AdvanceService.get_all_advances()
        return Response({
            "data": AdvanceService.serialize_advances(advances),
            "message": "Advance list retrieved successfully"
        }, status=status.HTTP_200_OK)


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