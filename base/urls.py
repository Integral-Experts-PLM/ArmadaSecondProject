from django.urls import path

from .views.incident_views import create_incident_views, read_incidents_views
from .views.maintenance_logs_views import create_maintenance_log_views, read_maintenance_logs_views
from .views import home_views, system_views, configuration_views, items_views   

urlpatterns = [
    # home
    path('', home_views.home, name='home'),

    # auxiliary path, only get data, no page render
    path('get-systems/', system_views.get_systems, name='get_systems'),
    path('get-configurations/', configuration_views.get_configurations, name='get_configurations'),

    # read
    path('search-incidents', read_incidents_views.search_incidents, name='search_incidents'),
    path('view-incidents/', read_incidents_views.view_incidents, name='view_incidents'),
    # path('view-all-incidents/', read_incidents_views.viewAllIncidents, name='view_all_incidents'),
    path('view-incident/', read_incidents_views.viewIncident, name='view_incident'),
    # path('view-maintenance-logs/', read_maintenance_logs_views.viewMaintenanceLogs, name='view_maintenance_logs'),
    path('search-incidents-logs/',read_maintenance_logs_views.search_incidents, name='search_incidents_logs'),
    path('view-incidents-logs/',read_maintenance_logs_views.view_incidents, name='view_incidents_logs'),
    path('get-maintenance-logs/',read_maintenance_logs_views.get_maintenance_logs, name='get_maintenance_logs'),
    path('view-maintenance-logs/',read_maintenance_logs_views.view_maintenance_logs, name='view_maintenance_logs'),
    path('get-tree-items/', items_views.get_tree_items, name='get_tree_items'),

    # creation
    path('create-incident/', create_incident_views.createIncident, name='create_incident'),
    path('create-maintenance-log/', create_maintenance_log_views.createMaintenanceLog, name='create_maintenance_log'),

]