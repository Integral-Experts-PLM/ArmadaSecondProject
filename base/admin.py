from django.contrib import admin

# Register your models here.
from .models import Incident
from .models import MaintenanceLog
from .models import OperatingTime

admin.site.register(Incident)
admin.site.register(MaintenanceLog)
admin.site.register(OperatingTime)