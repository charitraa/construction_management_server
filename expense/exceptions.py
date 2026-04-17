from rest_framework import status
from rest_framework.exceptions import APIException


class ExpenseNotFoundException(APIException):
    status_code = 404
    default_detail = "Expense not found."