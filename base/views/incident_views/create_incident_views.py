import requests
from datetime import datetime
import json
from django.conf import settings
from django.shortcuts import render, redirect
from ...forms import CreateIncidentForm
from ...web_services import get_projects

auth = (settings.API_USERNAME, settings.API_PASSWORD)


# Crreación de ioncidencias provisional hasta disponer de todos los campos
def createIncident(request):
    allProjects = get_projects()
    create_incident_form = CreateIncidentForm(request.POST or None)
    if request.method == 'POST':
        if create_incident_form.is_valid():
            project_id = request.POST.get('project_id')
            system_id = request.POST.get('system_id')
            configuration_id = request.POST.get('configuration_id')

            # TreeItem actualmente hardcodeado, se obtendrá de una lógica de Atavia
            # tree_item_id = 11068
            tree_item_id = 1031
            # Create forms for the incident creation
            create_incident_details = create_incident_form.save(commit=False)
            # Define base URL
            base_url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/'

            # Define the URL for creating an incident
            url_post = f'{base_url}Incidents'

            #provisional, para guardar hora en que se ha creado la incidencia en el campo Occurrence Date
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S+01:00")

            # Define the payload for creating an incident
            payload = {
                #provisional, hora en que se ha creado la incidencia
                "OccurrenceDate": formatted_time,
                
                "DescriptionIncident": create_incident_details.description_incident,
                "Configuration@odata.bind": f"Systems({system_id})/Configurations({configuration_id})",
                "SystemTreeItem@odata.bind": f"Systems({system_id})/TreeItems({tree_item_id})"
            }
            # Convert the payload dictionary to a JSON string
            payload_json = json.dumps(payload)

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Make the POST request to create an incident
            response = requests.post(
                url_post, data=payload_json, headers=headers, auth=auth)
            # Check the response
            if response.status_code == 201:
                data = response.json()
            else:
                print(
                    f"Failed to create incident. Status code: {response.status_code}")
                # Print the response content for debugging
                print(response.text)

        else:
            print("form not valid")

    context = {'allProjects': allProjects}
    return render(request, 'base/incidents/incident_create.html', context)
