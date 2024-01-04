from datetime import datetime
import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from ...db_queries import get_all_incidents, get_tree_name
from ...web_services import get_projects
from django.core.paginator import Paginator
from ...templatetags.custom_filters import format_datetime
import re


def search_incidents(request, message=None):
    # message = None
    allProjects = get_projects()
    context = {'allProjects': allProjects, 'message': message}
    return render(request, 'base/incidents/search_incidents.html', context)
    
def view_incidents(request):
    set_id = request.GET.get('system_id')
    conf_id = request.GET.get('configuration_id')
    tree_id = request.GET.get('tree_item_id')
    inc_identifier = request.GET.get('inc_identifier')
    inc_user = request.GET.get('inc_user')

    # Recoger parámetros de filtrado
    filter_column = request.GET.get('filter_column')
    filter_value = request.GET.get('filter_value')

    if set_id:
        incidents_data = get_all_incidents(set_id, conf_id, tree_id, inc_identifier, inc_user)
        if incidents_data is None:
            incidents_data = [] # para que incidents_data siempre sea una secuencia iterable incluso si está vacía antes de pasarla al Paginator. 
       
        # Añadir el nombre del TreeItem a cada incidencia
        for incident in incidents_data:
            incident.TreeName = incident.TreeID.Name

        # Filtrar incidents_data basándose en filter_column y filter_value
        if filter_column and filter_value:
            incidents_data = filter_incidents(incidents_data, filter_column, filter_value)

        paginator = Paginator(incidents_data, 50)  # 50 incidentes por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        start_number = (page_obj.number - 1) * 50
        context = {'page_obj': page_obj, 'start_number': start_number}
        return render(request, 'base/incidents/view_incidents.html', context)
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
