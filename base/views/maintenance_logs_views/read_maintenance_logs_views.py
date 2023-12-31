from datetime import datetime
import requests
import re
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from ...web_services import get_projects
from ...db_queries import get_all_incidents, get_tree_name, get_all_incidents_NotOptimized
from django.core.paginator import Paginator
from ...templatetags.custom_filters import format_datetime

auth = (settings.API_USERNAME, settings.API_PASSWORD)


def search_incidents(request, message=None):
    # message = None
    allProjects = get_projects()
    context = {'allProjects': allProjects, 'message': message}
    return render(request, 'base/maintenance_logs/search_incidents_logs.html', context)

def view_incidents(request):
    project_id = request.GET.get('project_id')
    request.session['project_id'] = project_id
    set_id = request.GET.get('system_id')
    request.session['system_id'] = set_id
    configuration_id = request.GET.get('configuration_id')
    tree_id = request.GET.get('tree_item_id')

    # Recoger parámetros de filtrado
    filter_column = request.GET.get('filter_column')
    filter_value = request.GET.get('filter_value')

    if set_id:
        incidents_data = get_all_incidents(set_id, configuration_id, tree_id)
        # incidents_data = get_all_incidents_NotOptimized(set_id, configuration_id, tree_id)
        if incidents_data is None:
            incidents_data = [] # incidents_data siempre sea una secuencia iterable incluso si está vacía antes de pasarla al Paginator. 

        for incident in incidents_data:
            incident.TreeName = incident.TreeID.Name
            # incident.TreeName = get_tree_name(incident.TreeID.ID)

        # Filtrar incidents_data basándose en filter_column y filter_value
        if filter_column and filter_value:
            incidents_data = filter_incidents(incidents_data, filter_column, filter_value)

        paginator = Paginator(incidents_data, 50)  # 50 incidentes por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        start_number = (page_obj.number - 1) * 50
        context = {'page_obj': page_obj, 'start_number': start_number}
        return render(request, 'base/maintenance_logs/view_incidents_logs.html', context)
    else:
        message = 'Clase y Serie son campos obligatorios'
        return search_incidents(request, message=message)

def filter_incidents(incidents, column, value):
    filtered_incidents = []

    for incident in incidents:
        attribute_value = getattr(incident, column, None)

        # Comprobar si el atributo es una instancia de datetime
        if isinstance(attribute_value, datetime):
            # Formatear la fecha y comparar
            if format_datetime(attribute_value) == value:
                filtered_incidents.append(incident)
        else:
            pattern = r'~[^:]+:.+'  # Patrón para ~texto:texto (~SEVERITY:CRITICAL)
            if isinstance(attribute_value, str) and re.match(pattern, attribute_value):
                # Tomar el texto después de los dos puntos
                attribute_value = attribute_value.split(':', 1)[1]

            # Para otros tipos de datos, realizar una comparación directa
            if str(attribute_value).lower() == value.lower():
                filtered_incidents.append(incident)

    return filtered_incidents


def view_maintenance_logs(request):
    incident_ID = request.session.get('incident_ID', '')
    maintenance_logs_data = request.session.get('maintenance_logs_data', [])

    # Prepara el mensaje basado en si hay datos de mantenimiento disponibles
    message = "No maintenance logs available" if not maintenance_logs_data else None

    context = {
        'maintenance_logs_data': maintenance_logs_data,
        'incident_ID': incident_ID,
        'message': message,
        'page': 'maintenance-logs',
    }
    
    # Borra los datos de la sesión si ya no son necesarios
    # del request.session['maintenance_logs_data']
    # del request.session['incident_ID']

    return render(request, 'base/maintenance_logs/maintenance_logs.html', context)


def get_maintenance_logs(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.body.decode('utf-8')
    request.session['incident_ID'] =incident_ID

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}/MaintenanceLogs'

    context = {
        'maintenance_logs_data': None,
        'incident_ID': incident_ID,
        'message': None,
    }

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        # Check if "value" property exists
        if 'value' in data:
            # Extract the "value" property
            context['maintenance_logs_data'] = data['value']
            request.session['maintenance_logs_data'] = data['value']
        else:
            return JsonResponse({'error': 'There is no "value" on this data'}, status=404)

        if not len(context['maintenance_logs_data']):
            context['message'] = "There are no maintenance logs yet!"
    else:
        return JsonResponse({'error': 'No maintenance logs available'}, status=404)
    
    if 'maintenance_logs_data' not in context:
        context['maintenance_logs_data'] = []
    
    return JsonResponse(context)
