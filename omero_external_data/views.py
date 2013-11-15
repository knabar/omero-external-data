import json

from django.http import Http404, HttpResponse

from omeroweb.webclient.decorators import login_required, render_response
from omero.gateway import TermAnnotationWrapper

import settings
from mocked import get_datasource_types


def fetch_annotations(conn, obj_dtype, obj_id):
    """
    Return the first available annotation for the given object in this app's
    namespace, or None if no annotation exists.
    """
    annotations = conn.getAnnotationLinks(
        obj_dtype, [obj_id], ns=settings.ANNOTATION_NAMESPACE)
    for annotation in annotations:
        yield annotation.getAnnotation()


TEMP = 1

def fetch_datasources(conn, obj_dtype, obj_id):
    for annotation in fetch_annotations(conn, obj_dtype, obj_id):
        datasource = json.loads(annotation.getValue())
        datasource["name"] = 'datasource%s' % TEMP
        global TEMP
        TEMP += 1
        yield datasource


def store_datasource(conn, obj_dtype, obj_id, datasource):
    obj = conn.getObject(str(obj_dtype), obj_id)
    TermAnnotationWrapper.createAndLink(
        obj, settings.ANNOTATION_NAMESPACE, val=datasource)


@login_required()
@render_response()
def index(request, obj_dtype, obj_id, conn=None, **_kwargs):

    template = "omero_external_data/omero_external_data.html"
    error = ""

    if request.method == 'POST':

        if request.GET.has_key('add_datasource'):

            datasource = json.dumps({
                'type': request.POST.get('datasource_type'),
                'inputs': {
                    'name': 'value'
                },
            })

            store_datasource(conn, obj_dtype, obj_id, datasource)

        #
        #if annotation and request.GET.has_key('delete'):
        #    obj = conn.getObject(str(obj_dtype), obj_id)
        #    obj.removeAnnotations(merckeln.settings.ANNOTATION_NAMESPACE)
        #    annotation = None

        #else:
        #
        #    try:
        #        eln_id = str(request.POST.get('eln_id'))
        #
        #        if not is_valid_eln_id(eln_id):
        #            raise ValueError
        #
        #        if annotation:
        #            annotation.setValue(eln_id)
        #            annotation.save()
        #        else:
        #            obj = conn.getObject(str(obj_dtype), obj_id)
        #            TermAnnotationWrapper.createAndLink(
        #                obj, merckeln.settings.ANNOTATION_NAMESPACE, val=eln_id)
        #            annotation = fetch_annotation(conn, obj_dtype, obj_id)
        #
        #    except ValueError:
        #        error = 'Invalid ELN identifier'


    datasources = fetch_datasources(conn, obj_dtype, obj_id)

    datasource_types = get_datasource_types(obj_dtype)

    context = {
        'obj_dtype': obj_dtype,
        'obj_id': obj_id,
        'error': error,
        'datasources': datasources,
        'datasource_types': datasource_types,
    }

    context['template'] = template
    return context


@login_required()
@render_response()
def load_datasource(request, obj_dtype, obj_id, conn=None, **_kwargs):

    return "Test for %s %s %s" % (obj_dtype, obj_id, request.GET.get('datasource'))

@login_required()
@render_response()
def delete_datasource(request, obj_dtype, obj_id, conn=None, **_kwargs):

    return dict(bad='true', errs='Deleting not supported yet')
