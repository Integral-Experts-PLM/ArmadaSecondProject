from django.conf import settings
import requests
from django.shortcuts import render, redirect

#===========================================================================
# global credentials to be used on all calls
auth = (settings.API_USERNAME, settings.API_PASSWORD)

# get projects to populate the dropdowns
def get_projects():
    getProjectsUrl = 'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/ProjectMgmt/Projects'
    try:
        response = requests.get(getProjectsUrl, auth=auth)
        if response.status_code == 200:
            allProjects = response.json()
            return allProjects
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def home(request):
    # message = None  # Initialize the message variable
    # allProjects = get_projects()

    # if request.method == 'POST':
    #     project_id = request.POST.get('project_id')
    #     project_name = request.POST.get('project_name')
    #     system_id = request.POST.get('system_id')
    #     system_name = request.POST.get('system_name')
    #     print('sysHome', system_name)
    #     configuration_id = request.POST.get('configuration_id')
    #     configuration_name = request.POST.get('configuration_name')
    #     tree_item_id = request.POST.get('tree_item_id')
    #     tree_item_name = request.POST.get('tree_item_name')

    #     incidents = None
    #     #  tree_item_id == '0' means no item selected
    #     if project_id and system_id and configuration_id and tree_item_id == '0':
    #         url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents?$expand=Configuration,SystemTreeItem'
    #         response = requests.get(url, auth=auth)

    #         if response.status_code == 200:
    #             data = response.json()
    #             incidents = [incident for incident in data['value'] if incident['Configuration'].get('ID') == int(configuration_id)]

    #     elif project_id and system_id and configuration_id and tree_item_id != '0':
    #         url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents?$expand=Configuration,SystemTreeItem'
    #         response = requests.get(url, auth=auth)

    #         if response.status_code == 200:
    #             data = response.json()
    #             incidents = [incident for incident in data['value'] if incident['Configuration'].get('ID') == int(configuration_id) and incident['SystemTreeItem']['ID'] == int(tree_item_id)]

    #     # Store the values in the session - only store incident ID if the combination produces at least one incident
    #     if incidents:
    #         request.session['incident_ID'] = incidents[0]['ID']
    #         # Create ans store a dictionary with ID as the key so we can access a specific incident without calling the web service
    #         incidents_dict = {incident["ID"]: incident for incident in incidents}
    #         request.session['incidents_dict'] = incidents_dict
            
    #     request.session['project_id'] = project_id
    #     request.session['project_name'] = project_name
    #     request.session['system_id'] = system_id
    #     request.session['system_name'] = system_name
    #     request.session['configuration_id'] = configuration_id
    #     request.session['configuration_name'] = configuration_name
    #     request.session['tree_item_id'] = tree_item_id
    #     request.session['tree_item_name'] = tree_item_name
    #     context = {
    #         'incidents_data': incidents,
    #         'page': 'view-all-incidents',
    #     }
    #     request.session['context_data'] = context
    #     return redirect('view_all_incidents')
    
    # context = {'message': message, 'allProjects': allProjects}

    context = {}
    return render(request, 'base/home.html', context)
