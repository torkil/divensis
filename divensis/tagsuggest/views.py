from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

import simplejson as json

from tagging.models import Tag


def search_tags(request):
    try:
        search_term = '%s' % request.GET['search']
        if len(search_term) != 0:
            tags = Tag.objects.filter(Q(name__icontains=search_term))
            result = []
            for tag in tags:
                result.append([tag.name, tag.name, tag.name])
        return HttpResponse(json.dumps(result, separators=(',',':')), mimetype='application/json')
    except MultiValueDictKeyError:
        pass