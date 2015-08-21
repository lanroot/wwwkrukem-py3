# -*- coding: utf8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db.models import Q
from haystack.query import SearchQuerySet
from userdir.models import Person, City, Div

import json
import logging
import urllib

logr = logging.getLogger(__name__)

_eng_chars = u"~!@$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ё!\";%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_trans_table = dict(zip(_eng_chars, _rus_chars))
 
def fix_layout(s):
    return u''.join([_trans_table.get(c, c) for c in s])

def persons(request):

    args = {}
    args.update(csrf(request))

    args['persons'] = Person.objects.filter(visible=1)

    return render_to_response('persons.html',
            RequestContext(request, args)
            )

def person(request, person_id=1):
    div_id = Person.objects.get(pers_id=person_id).div_id
    city_id = Div.objects.get(id=div_id).city_id

    return render_to_response('person.html',
            RequestContext(request, ({ 'person': Person.objects.get(pers_id=person_id),
                'div': Div.objects.get(id=div_id),
                'city': City.objects.get(id=city_id) 
                                    })
                            )
            )

def search_persons_cp1251(request):

    request.encoding = 'cp1251'
    search_text = request.GET['sh']

    args = {}
    args.update(csrf(request))

    args['persons'] = Person.objects.filter(Q(visible=1), Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(mtel__icontains=search_text)| Q(office__contains=search_text) | Q(post__icontains=search_text) | Q(subdiv__icontains=search_text))

    logr.debug(persons)

    return render_to_response('persons.html', RequestContext(request, args))

def search_persons(request):

    search_text = request.GET['sh']
    search_text_wrong_layout = fix_layout(search_text)

    args = {}
    args.update(csrf(request))

    args['persons'] = Person.objects.filter(Q(visible=1), Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(mtel__icontains=search_text)| Q(office__contains=search_text) | Q(post__icontains=search_text) | Q(subdiv__icontains=search_text) | Q(name__icontains=search_text_wrong_layout))
    logr.debug(persons)

    args['search_text'] = search_text

    return render_to_response('persons.html', RequestContext(request, args))

def autocomplete(request):

    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:15]
    suggestions = [{'label': (result.name, result.email), 'value': result.pers_id} for result in sqs]
# Make sure you return a JSON object, not a base list.
# Otherwise, you could be vulnerable to an XSS attack.
#    the_data = json.dumps({
#        'results': suggestions
#    })

    return HttpResponse(json.dumps(suggestions), content_type='application/json')
