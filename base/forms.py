from django.forms import ModelForm
from .models import CreateIncident, MaintenanceLog

class CreateIncidentForm(ModelForm):
    class Meta:
        model = CreateIncident
        exclude = ['user_text22_failure_evidence', 'user_text23_failure_evidence', 'user_text24_failure_evidence', 'user_text25_failure_evidence',
                   'identifier', 'system_tree_item', 'name', 'user_text26_user_failure_detection', 'occurrence_time', 'occurrence_date']


class MaintenanceLogForm(ModelForm):
    class Meta:
        model = MaintenanceLog
        exclude = ['incident_ID', 'maintenance_log_identifier']
