from django.db import models

class CreateIncident(models.Model):
    project_id = models.CharField(max_length=200)
    system_id = models.CharField(max_length=200)
    configuration_id = models.CharField(max_length=200,)
    system_tree_item = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    user_text22_failure_detection_situation = models.CharField(max_length=200, null=True, blank=True)
    user_text23_failure_buque_situation = models.CharField(max_length=200, null=True, blank=True)
    user_text24_failure_effect_item = models.CharField(max_length=200, null=True, blank=True)
    user_text25_failure_evidence = models.CharField(max_length=200, null=True, blank=True)
    occurrence_date = models.DateTimeField()
    occurrence_time = models.CharField(max_length=200, null=True, blank=True)
    description_incident =  models.TextField(null=True, blank=True)
    user_text26_user_failure_detection = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
    
class MaintenanceLog(models.Model):
    incident_ID = models.CharField(max_length=200)
    maintenance_log_identifier = models.CharField(max_length=200)
    override_system_tree_item_replaced_part = models.CharField(max_length=200, null=True, blank=True)
    cost_item = models.FloatField(null=True, blank=True)
    number_of_men = models.IntegerField(null=True, blank=True)
    elapsed_maintenance_time = models.FloatField(null=True, blank=True)
    action_taken_maintenace = models.CharField(max_length=200, null=True, blank=True)
    total_maintenance_time = models.FloatField(null=True, blank=True)
    user_value2_total_maintenance_time = models.FloatField(null=True, blank=True)
    cost_maintenance = models.FloatField(null=True, blank=True)
    maintenance_start_date = models.DateTimeField()

    def __str__(self):
        return str(self.maintenance_log_identifier)
    
