from django.forms import ModelForm
from .models import Incident, MaintenanceLog, OperatingTime

# 'incident_ID' must be exclude because it is asign automaticaly
class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        exclude = ['identifier', 'project_id', 'system_id', 'configuration', 'system_tree_item', 'name', 'user_text26_user_failure_detection', 'occurrence_time']

class MaintenanceLogForm(ModelForm):
    class Meta:
        model = MaintenanceLog
        exclude = ['incident_ID', 'maintenance_log_identifier']

# 'operational_time' must be exclude because it not editable
class OperatingTimeForm(ModelForm):
    class Meta:
        model = OperatingTime
        exclude = ['operational_time']
