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
import pandas as pd
from django.http import HttpResponse
from django.forms.models import model_to_dict
from datetime import datetime


def search_incidents(request, message=None):
    request.session.clear()

    allProjects = get_projects()
    context = {'allProjects': allProjects, 'message': message}

    if request.method == 'POST':
        print('post')
        # Set mandatory session variables
        request.session['project_id'] = request.POST.get('project_id')
        request.session['system_id'] = request.POST.get('system_id')

        # Set other session variables if provided
        if 'configuration_id' in request.POST:
            request.session['configuration_id'] = request.POST.get('configuration_id')
        if 'tree_item_id' in request.POST:
            request.session['tree_item_id'] = request.POST.get('tree_item_id')
        if 'inc_identifier' in request.POST:
            request.session['inc_identifier'] = request.POST.get('inc_identifier')
        if 'inc_user' in request.POST:
            request.session['inc_user'] = request.POST.get('inc_user')

        # Redirect to the view_incidents view after setting the session variables
        return redirect('view_incidents')

    return render(request, 'base/incidents/search_incidents.html', context)
    
def view_incidents(request):
    set_id = request.session.get('system_id')
    conf_id = request.session.get('configuration_id')
    tree_id = request.session.get('tree_item_id')
    inc_identifier = request.session.get('inc_identifier')
    inc_user = request.session.get('inc_user')

    if not set_id:
        message = 'Clase y Serie son campos obligatorios'
        return search_incidents(request, message=message)

    incidents_data = get_all_incidents(set_id, conf_id, tree_id, inc_identifier, inc_user)
    if incidents_data is None:
        incidents_data = [] # para que incidents_data siempre sea una secuencia iterable incluso si está vacía antes de pasarla al Paginator. 

    # Añadir el nombre del TreeItem a cada incidencia
    for incident in incidents_data:
        incident.TreeName = incident.TreeID.Name

    # Initialize filter parameters
    filter_params = {
        'ID': request.GET.get('ID'),
        'Identifier': request.GET.get('Identifier'),
        'IncidentUser': request.GET.get('IncidentUser'),
        'DateIncident': request.GET.get('DateIncident'),
        'DateEndCO': request.GET.get('DateEndCO'),
        'IncUserText2': request.GET.get('IncUserText2'),
        'IncidentDescription': request.GET.get('IncidentDescription'),
        'TreeName': request.GET.get('TreeName'),
    }

    # Conversión a diccionario de la lista de incidencias para permitir la exportación a Excel
    incidents_list = [convert_to_dict(incident) for incident in incidents_data]
    # request.session['all_incidents'] = incidents_list
    request.session['filtered_incidents'] = incidents_list # por si no se aplica ningún filtro (para la exportación a Excel)

    # Aplicar filtros
    for key, value in filter_params.items():
        if value:
            incidents_data = filter_incidents(incidents_data, key, value)
            filtered_list = [convert_to_dict(incident) for incident in incidents_data]
            request.session['filtered_incidents'] = filtered_list

    paginator = Paginator(incidents_data, 50)  # 50 incidentes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    start_number = (page_obj.number - 1) * 50
    context = {'page_obj': page_obj, 'start_number': start_number}
    return render(request, 'base/incidents/view_incidents.html', context)
    
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

def export_incidents_to_excel(request):
    incidents_data = request.session.get('filtered_incidents', [])
    df = pd.DataFrame(incidents_data)

    # Renombrar las columnas del Excel, igualarlas al html
    column_name_mapping = {
        '':'',
        'ID': 'ID',
        'Identifier': 'Identificador',
        'IncidentUser': 'Reportado por',
        'DateIncident': 'Fecha del fallo',
        'DateEndCo': 'Fecha del cierre',
        'IncUserText2': 'Severidad inicial',
        'IncidentDescription': 'Descripción',
        'HSC': 'HSC'
    }
    df.rename(columns=column_name_mapping, inplace=True)

    timestamp = datetime.now().strftime("%d-%m-%Y")
    # Convert the DataFrame to an Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="incidents_{timestamp}.xlsx"'

    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        # Formato para centrar el texto
        center_format = writer.book.add_format({'align': 'center', 'valign': 'vcenter'})
        df.to_excel(writer, index=False, sheet_name='Incidents', startrow=1, header=False)
        worksheet = writer.sheets['Incidents']

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, center_format)

        for row_num in range(1, len(df) + 1):
            for col_num in range(len(df.columns)):
                worksheet.write(row_num, col_num, df.iloc[row_num - 1, col_num], center_format)

        # Ajustar ancho de columnas, excepto Descripción
        for column in df:
            if column != 'Descripción':
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                worksheet.set_column(col_idx, col_idx, column_length)

    return response



def convert_to_dict(instance):
    instance_dict = model_to_dict(instance)

    # Convertir objetos datetime a texto d/m/a
    for key, value in instance_dict.items():
        if isinstance(value, datetime):
            instance_dict[key] = value.strftime('%d/%m/%Y')
    
    instance_dict['HSC'] = instance.TreeName

    return instance_dict