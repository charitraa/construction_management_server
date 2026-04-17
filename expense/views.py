from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.permission import HasPageAccess
from core.permission import LoginRequiredPermission
from .serializers import (
    ExpenseSerializer,
    ExpenseCreateSerializer,
    ExpenseUpdateSerializer
)
from .services import ExpenseService
from .exceptions import ExpenseNotFoundException
import csv
import io


class ExpenseListView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, *args, **kwargs):
        expenses = ExpenseService.get_all_expenses()
        return Response({
            "data": ExpenseService.serialize_expenses(expenses),
            "message": "Expense list retrieved successfully"
        }, status=status.HTTP_200_OK)


class ExpenseCreateView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def post(self, request, *args, **kwargs):
        serializer = ExpenseCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            expense = serializer.save()
            return Response({
                "data": ExpenseService.serialize_expense(expense),
                "message": "Expense created successfully"
            }, status=status.HTTP_201_CREATED)


class ExpenseRetrieveView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, expense_id, *args, **kwargs):
        expense = ExpenseService.get_expense_by_id(expense_id)
        if not expense:
            raise ExpenseNotFoundException("Expense not found.")
        return Response({
            "data": ExpenseService.serialize_expense(expense),
            "message": "Expense details retrieved successfully"
        }, status=status.HTTP_200_OK)


class ExpenseUpdateView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def put(self, request, expense_id, *args, **kwargs):
        expense = ExpenseService.get_expense_by_id(expense_id)
        if not expense:
            raise ExpenseNotFoundException("Expense not found.")
        serializer = ExpenseUpdateSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            expense = serializer.save()
            return Response({
                "data": ExpenseService.serialize_expense(expense),
                "message": "Expense updated successfully"
            }, status=status.HTTP_200_OK)


class ExpenseDestroyView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def delete(self, request, expense_id, *args, **kwargs):
        expense = ExpenseService.get_expense_by_id(expense_id)
        if not expense:
            raise ExpenseNotFoundException("Expense not found.")
        ExpenseService.delete_expense(expense)
        return Response({
            "message": "Expense deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class ExpenseStatsView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, *args, **kwargs):
        stats = ExpenseService.get_expense_stats()
        return Response({
            "data": stats,
            "message": "Expense statistics retrieved successfully"
        }, status=status.HTTP_200_OK)


class ExpenseExportView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        expenses = ExpenseService.get_all_expenses()
        
        if category:
            expenses = expenses.filter(category=category)
        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])
        
        if not expenses.exists():
            return Response({
                "error": "No expenses to export"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Description', 'Category', 'Amount'])
        
        for exp in expenses:
            writer.writerow([exp.date, exp.description, exp.category, exp.amount])
        
        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Expenses exported successfully"
        }, status=status.HTTP_200_OK)