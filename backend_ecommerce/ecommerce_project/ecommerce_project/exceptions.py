from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that returns responses in a standard format.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If unexpected error occurs (server error, etc.)
    if response is None:
        return Response(
            {'error': 'An unexpected error occurred.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Format the response data
    if isinstance(exc, Http404):
        response.data = {'error': 'Resource not found.'}
    elif isinstance(exc, NotAuthenticated):
        response.data = {'error': 'Authentication required.'}
    elif isinstance(exc, PermissionDenied):
        response.data = {'error': 'You do not have permission to perform this action.'}
    elif response.data and isinstance(response.data, dict):
        if 'detail' in response.data:
            response.data = {'error': response.data['detail']}
    
    return response