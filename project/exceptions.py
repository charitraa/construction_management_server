from rest_framework import status
from rest_framework.exceptions import APIException


class ProjectNotFoundException(APIException):
    status_code = 404
    default_detail = "Project not found."