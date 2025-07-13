import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import QualityLog
from .serializers import QualityLogSerializer

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def staff_login(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    logger.info(f"Login attempt for username: {username}")

    # Create or update user with provided username and password, set as staff and active
    user, created = User.objects.get_or_create(username=username)
    user.is_staff = True
    user.is_active = True
    user.set_password(password)
    user.save()

    # Authenticate user after setting password
    user = authenticate(request, username=username, password=password)

    if user is not None:
        logger.info(f"User authenticated: {username}, is_staff: {user.is_staff}, is_active: {user.is_active}")
        login(request, user)
        logger.info(f"User logged in: {username}")
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        logger.warning(f"Invalid credentials for username: {username}")
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

import os
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import QualityLog
from .serializers import QualityLogSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def staff_login(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    logger.info(f"Login attempt for username: {username}")

    # Create or update user with provided username and password, set as staff and active
    user, created = User.objects.get_or_create(username=username)
    user.is_staff = True
    user.is_active = True
    user.set_password(password)
    user.save()

    # Authenticate user after setting password
    user = authenticate(request, username=username, password=password)

    if user is not None:
        logger.info(f"User authenticated: {username}, is_staff: {user.is_staff}, is_active: {user.is_active}")
        login(request, user)
        logger.info(f"User logged in: {username}")
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        logger.warning(f"Invalid credentials for username: {username}")
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tvecs_logs(request):
    user = request.user
    if user.is_authenticated:
        logger.info(f"Authenticated request by user: {user.username}")
    else:
        logger.warning("Unauthenticated request to tvecs_logs")

    logs = QualityLog.objects.all()

    # Get filter parameters from query params
    body_no = request.query_params.get('body_no')
    start_date_time = request.query_params.get('start_date_time')
    end_date_time = request.query_params.get('end_date_time')
    date_time = request.query_params.get('date_time')
    total_result = request.query_params.get('total_result')

    # Filter queryset based on provided parameters
    if body_no:
        logs = logs.filter(body_no__icontains=body_no)
    if date_time:
        # Assuming date_time filter is exact match or date part only
        logs = logs.filter(date_time__startswith=date_time)
    if start_date_time:
        logs = logs.filter(date_time__gte=start_date_time)
    if end_date_time:
        logs = logs.filter(date_time__lte=end_date_time)
    if total_result:
        logs = logs.filter(total_result__icontains=total_result)

    logs = logs.order_by('-date_time')
    serializer = QualityLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request):
    file_path = request.query_params.get('file_path')
    if not file_path:
        return Response({'error': 'file_path parameter is required'}, status=400)

    # Validate file path to prevent directory traversal attacks
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    abs_file_path = os.path.abspath(file_path)
    if not abs_file_path.startswith(base_dir):
        return Response({'error': 'Invalid file path'}, status=400)

    if not os.path.exists(abs_file_path):
        return Response({'error': 'File not found'}, status=404)

    try:
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Error reading file {abs_file_path}: {e}")
        return Response({'error': 'Error reading file'}, status=500)

    response = HttpResponse(content, content_type='text/csv')
    filename = os.path.basename(abs_file_path)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
