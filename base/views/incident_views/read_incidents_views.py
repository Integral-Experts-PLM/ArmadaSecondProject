import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from ...db_queries import get_all_incidents, get_tree_name
from ...web_services import get_projects
from django.core.paginator import Paginator


def search_incidents(request, message=None):
    # message = None
    allProjects = get_projects()
    context = {'allProjects': allProjects, 'message': message}
    return render(request, 'base/incidents/search_incidents.html', context)
    
def view_incidents(request):
    set_id = request.GET.get('system_id')
    configuration_id = request.GET.get('configuration_id')
    tree_id = request.GET.get('tree_item_id')

    # Recoger parámetros de filtrado
    filter_column = request.GET.get('filter_column')
    filter_value = request.GET.get('filter_value')
    print(filter_column)
    print(filter_value)

    if set_id:
        incidents_query = get_all_incidents(set_id, configuration_id, tree_id)
        if incidents_query is None:
            incidents_query = [] # para que incidents_data siempre sea una secuencia iterable incluso si está vacía antes de pasarla al Paginator. 

        # Convertir QuerySet a una lista de diccionarios
        incidents_data = [incident_to_dict(incident) for incident in incidents_query]

        print(incidents_data)
        # Aplicar filtro en la vista
        if filter_column and filter_value:
            incidents_data = [incident for incident in incidents_data if str(incident.get(filter_column, '')).lower() == filter_value.lower()]

        # Filtrar los datos de incidentes
        # if filter_column and filter_value:
        #     filtered_incidents = []
        #     for incident in incidents_data:
        #         # Obtener el valor del atributo del incidente
        #         incident_value = getattr(incident, filter_column, '')
        #         # Comprobar si el valor coincide con el filtro
        #         if str(incident_value).lower() == filter_value.lower():
        #             filtered_incidents.append(incident)
        #     incidents_data = filtered_incidents

        # Añadir el nombre del TreeItem a cada incidencia
        # for incident in incidents_data:
        #     incident.TreeName = incident.TreeID.Name

        
        paginator = Paginator(incidents_data, 50)  # 50 incidentes por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        start_number = (page_obj.number - 1) * 50
        context = {'page_obj': page_obj, 'start_number': start_number}
        return render(request, 'base/incidents/view_incidents.html', context)
    else:
        message = 'Clase y Serie son campos obligatorios'
        return search_incidents(request, message=message)


def incident_to_dict(incident):
    # Implementa la conversión del objeto 'Incident' a un diccionario
    # Esto puede incluir la conversión de objetos relacionados y campos especiales
    return {
        'ID': incident.ID,
        'Identifier': incident.Identifier,
        'DateStart': incident.DateStart.strftime("%Y-%m-%d %H:%M:%S") if incident.DateStart else None,
        'SetID': incident.SetID,
        'ConfigurationID': incident.ConfigurationID,
        'TreeName': incident.TreeID.Name if incident.TreeID else None,
        # Agrega otros campos necesarios
    }

def viewIncident(request):
    if request.method == 'POST':
        incident_ID = request.body.decode('utf-8')
        request.session['incident_ID'] = incident_ID
        globalContext = request.session.get('context_data', {})
        globalContext['selectedIncidentId'] = incident_ID
        json_data = globalContext['incidents_data']
        # Set safe to False for non-dict objects
        return JsonResponse(json_data, safe=False)
