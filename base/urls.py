from django.urls import path

from .views.incident_views import create_incident_views, read_incidents_views
from .views.maintenance_logs_views import create_maintenance_log_views, read_maintenance_logs_views
from .views.operating_times_views import create_operating_time_views, read_operating_times_views
from .views import home_views, system_views, configuration_views

urlpatterns = [
    # home
    path('', home_views.home, name='home'),

    # auxiliary path, only get data, no page render
    path('get-systems/', system_views.get_systems, name='get_systems'),
    path('get-configurations/', configuration_views.get_configurations, name='get_configurations'),

    # read
    path('view-all-incidents/', read_incidents_views.viewAllIncidents, name='view_all_incidents'),
    path('view-incident/', read_incidents_views.viewIncident, name='view_incident'),
    path('view-maintenance-logs/', read_maintenance_logs_views.viewMaintenanceLogs, name='view_maintenance_logs'),
    path('view-operating-times/', read_operating_times_views.viewOperatingTimes, name='view_operating_times'),

    # creation
    path('create-incident/', create_incident_views.createIncident, name='create_incident'),
    path('create-maintenance-log/', create_maintenance_log_views.createMaintenanceLog, name='create_maintenance_log'),
    path('create-operating-time/', create_operating_time_views.createOperatingTime, name='create_operating_time'),

]