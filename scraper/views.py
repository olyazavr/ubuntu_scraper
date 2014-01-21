from django.views import generic
from django.template import RequestContext
from django.shortcuts import render_to_response 
from django.db.models import Q
import re

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



''' Splits the query string in invidual keywords, getting rid of unecessary spaces
    and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces'] '''
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


''' Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.'''
def get_query(query_string, search_fields):
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query