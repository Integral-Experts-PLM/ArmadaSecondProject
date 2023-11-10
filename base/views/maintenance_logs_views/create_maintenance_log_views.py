import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

auth = (settings.API_USERNAME, settings.API_PASSWORD)


def createMaintenanceLog(request):
    context = {}
    return render(request, 'base/maintenance_logs/maintenance_log_create.html', context)
