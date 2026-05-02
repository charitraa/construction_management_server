from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from core.permission import LoginRequiredPermission
from .serializers import (
    ExpenseCreateSerializer,
    ExpenseUpdateSerializer
)
from .services import ExpenseService
from .exceptions import ExpenseNotFoundException
import csv
import io


class ExpensePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ExpenseListView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        project = request.query_params.get('project')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        search = request.query_params.get('search')

        expenses = ExpenseService.get_all_expenses()

        if category:
            expenses = expenses.filter(category=category)
        if project and project != 'all':
            expenses = expenses.filter(project=project)
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)
        if search:
            expenses = expenses.filter(description__icontains=search)

        paginator = ExpensePagination()
        paginated_expenses = paginator.paginate_queryset(expenses, request)

        return paginator.get_paginated_response({
            "data": ExpenseService.serialize_expenses(paginated_expenses),
            "message": "Expense list retrieved successfully"
        })


class ExpenseCreateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, *args, **kwargs):
        serializer = ExpenseCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            expense = serializer.save()
            return Response({
                "data": ExpenseService.serialize_expense(expense),
                "message": "Expense created successfully"
            }, status=status.HTTP_201_CREATED)


class ExpenseRetrieveView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, expense_id, *args, **kwargs):
        expense = ExpenseService.get_expense_by_id(expense_id)
        if not expense:
            raise ExpenseNotFoundException("Expense not found.")
        return Response({
            "data": ExpenseService.serialize_expense(expense),
            "message": "Expense details retrieved successfully"
        }, status=status.HTTP_200_OK)


class ExpenseUpdateView(APIView):
    permission_classes = [LoginRequiredPermission]

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
    permission_classes = [LoginRequiredPermission]

    def delete(self, request, expense_id, *args, **kwargs):
        expense = ExpenseService.get_expense_by_id(expense_id)
        if not expense:
            raise ExpenseNotFoundException("Expense not found.")
        ExpenseService.delete_expense(expense)
        return Response({
            "message": "Expense deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class ExpenseStatsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        stats = ExpenseService.get_expense_stats()
        return Response({
            "data": stats,
            "message": "Expense statistics retrieved successfully"
        }, status=status.HTTP_200_OK)


class ExpenseExportView(APIView):
    permission_classes = [LoginRequiredPermission]

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