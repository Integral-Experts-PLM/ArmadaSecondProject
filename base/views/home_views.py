import requests
import time
from django.conf import settings
from django.shortcuts import render, redirect
from ..web_services import get_projects
   
def home(request):
    return render(request, 'base/home.html')
