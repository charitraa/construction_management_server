from rest_framework import status
from rest_framework.exceptions import APIException


class RevenueNotFoundException(APIException):
    status_code = 404
    default_detail = "Revenue record not found."