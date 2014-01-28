import slate
from django.db.models import Q
import re
import os
import glob

def parse_pdf(pdfDir):
    ''' Converts a pdf to text and returns the first page to be parsed 
    later. Pass in the directory the files are saved in, will parse the
    latest one every time.'''

    # super sketchy
    os.chdir(pdfDir)
    newest = max(glob.iglob('*.pdf'), key=os.path.getctime) # find the file just saved
    doc = []

    with open(newest) as pdf:
        doc = slate.PDF(pdf) # convert the pdf

    os.remove(newest) # delete when we're done
    return doc[0] # return first page for now

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
    and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces'] '''

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.'''

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