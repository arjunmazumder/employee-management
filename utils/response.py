# utils/response.py

from rest_framework.response import Response


def success_response(message, data=None, status_code=200):
    return Response({
        "message": message,
        "data": data,
        "errors": None
    }, status=status_code)


def error_response(message, errors=None, status_code=400):
    return Response({
        "message": message,
        "data": None,
        "errors": errors
    }, status=status_code)