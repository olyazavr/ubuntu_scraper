from django.views import generic
from django.template import RequestContext
from django.shortcuts import render_to_response 
from utils import get_query

from scraper.models import Hardware, Computer

class HardwareView(generic.DetailView):
    model = Hardware
    template_name = 'scraper/hardware.html'

class ComputerView(generic.DetailView):
    model = Computer
    template_name = 'scraper/computer.html'

''' Searches and displays the found results '''
def search(request):
	query_string = ''
	found_entries = None
	obj = ''
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['name'])
		obj = request.GET['type'] # either hardware or computer
		if obj == 'hardware':
			found_entries = Hardware.objects.filter(entry_query).order_by('name')
		else:
			found_entries = Computer.objects.filter(entry_query).order_by('name')
	return render_to_response('scraper/index.html',
                          { 'query_string': query_string, 'found_entries': found_entries, 'type' : obj},
                          context_instance=RequestContext(request))