import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

auth = (settings.API_USERNAME, settings.API_PASSWORD)


def viewAllIncidents(request):
    # incident_ID = None
    # incident_ID = request.session.get('incident_ID', 'default-incident-id')
    # globalContext = request.session.get('context_data', {})

    # if len(globalContext['incidents_data']) > 0:
    #     globalContext['selectedIncidentId'] = incident_ID
    # else:
    #     print('no incidents found')
    
    globalContext = {}
    return render(request, 'base/incidents/incidents.html', globalContext)


def viewIncident(request):
    if request.method == 'POST':
        # Get the selected incident ID from the POST request
        incident_ID = request.body.decode('utf-8')

        request.session['incident_ID'] = incident_ID
        globalContext = request.session.get('context_data', {})
        globalContext['selectedIncidentId'] = incident_ID
        json_data = globalContext['incidents_data']
        # Set safe to False for non-dict objects
        return JsonResponse(json_data, safe=False)
