from django.urls import path
from .views import staff_login, tvecs_logs

from .views import download_file

urlpatterns = [
    path('login/', staff_login, name='staff_login'),
    path('logs/', tvecs_logs, name='tvecs_logs'),
    path('download-file/', download_file, name='download_file'),
]
