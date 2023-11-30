from django.contrib import admin

# Register your models here.
from .models import CreateIncident
from .models import MaintenanceLog

admin.site.register(CreateIncident)
admin.site.register(MaintenanceLog)
