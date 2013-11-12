
from django.http import Http404, HttpResponse

from omeroweb.webclient.decorators import login_required, render_response

import settings


@login_required()
@render_response()
def index(request, obj_dtype, obj_id, conn=None, **_kwargs):

    template = "omero_external_data/omero_external_data.html"
    error = ""

    context = {
        'obj_dtype': obj_dtype,
        'obj_id': obj_id,
        'error': error,
    }

    context['template'] = template
    return context
