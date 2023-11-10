import requests
import json
from django.conf import settings
from django.shortcuts import render, redirect
from ...forms import IncidentForm

auth = (settings.API_USERNAME, settings.API_PASSWORD)


def createIncident(request):
    # project_id = request.session.get('project_id')
    # project_name = request.session.get('project_name')
    # system_id = request.session.get('system_id')
    # system_name = request.session.get('system_name')
    # configuration_name = request.session.get('configuration_name')
    # tree_item_name = request.session.get('tree_item_name')
    # tree_items_data = request.session.get('tree_items_data', [])

    # # Create forms for the incident creation
    # create_incident_form = IncidentForm(request.POST or None)

    # context = {
    #     'configuration_name': configuration_name,
    #     'tree_item_name': tree_item_name,
    #     'tree_items_data': tree_items_data,
    #     'create_incident_form': create_incident_form,
    #     'view': 'create_incident_forms'
    # }

    # # Define base URL
    # base_url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/'

    # configuration_id = request.session.get('configuration_id')
    # if configuration_id is not None:
    #     print(create_incident_form.is_valid())
    #     if request.method == 'POST' and create_incident_form.is_valid():

    #         tree_item_name = request.POST.get('tree_item_name', '')

    #         if request.session['tree_item_id'] != '0':
    #             tree_item_id = request.session['tree_item_id']
    #         else:
    #             tree_item_id = request.POST.get('tree_item_id', '')

    #         create_incident_details = create_incident_form.save(commit=False)
    #         # Define the URL for creating an incident
    #         url_post = f'{base_url}Incidents'

    #         # Define the payload for creating an incident
    #         payload = {
    #             "UserText22": create_incident_details.user_text22_failure_detection_situation,
    #             "UserText23": create_incident_details.user_text23_failure_buque_situation,
    #             "UserText24": create_incident_details.user_text24_failure_effect_item,
    #             "UserText25": create_incident_details.user_text25_failure_evidence,
    #             "OccurrenceDate": create_incident_details.occurrence_date.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
    #             # "OccurrenceTime": hour,
    #             "DescriptionIncident": create_incident_details.description_incident,

    #             "Configuration@odata.bind": f"Systems({system_id})/Configurations({configuration_id})",
    #             "SystemTreeItem@odata.bind": f"Systems({system_id})/TreeItems({tree_item_id})"
    #         }

    #         # Set the headers for the request
    #         headers = {
    #             "Content-Type": "application/json",
    #             "Accept": "application/json",
    #         }

    #         # Convert the payload dictionary to a JSON string
    #         payload_json = json.dumps(payload)

    #         # Make the POST request to create an incident
    #         response = requests.post(
    #             url_post, data=payload_json, headers=headers, auth=auth)
    #         print(payload_json)
    #         # Check the response
    #         if response.status_code == 201:
    #             data = response.json()
    #             if data:
    #                 data['SystemTreeItem'] = {'Name': tree_item_name}
    #                 request.session['incident_ID'] = data['ID']
    #                 if 'incidents_dict' not in request.session:
    #                     request.session['incidents_dict'] = {}

    #                 request.session['incidents_dict'][data['ID']] = data
    #                 request.session['context_data']['incidents_data'].append(
    #                     data)
    #             return redirect('incident_report')
    #         else:
    #             print(
    #                 f"Failed to create incident. Status code: {response.status_code}")
    #             # Print the response content for debugging
    #             print(response.text)
    #     else:
    #         context = {
    #             'project_name': project_name,
    #             'system_name': system_name,
    #             'configuration_name': configuration_name,
    #             'tree_item_name': tree_item_name,
    #             'tree_items_data': tree_items_data,
    #             'create_incident_form': create_incident_form,
    #             'view': 'create_incident_B'
    #         }
    # else:
    #     print("Failed to retrieve configuration and tree item data.")
    
    context = {}
    return render(request, 'base/incidents/incident_create.html', context)
