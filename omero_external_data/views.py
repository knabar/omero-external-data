import json

from django.http import Http404, HttpResponse
from django import forms

from omeroweb.webclient.decorators import login_required, render_response
from omero.gateway import TermAnnotationWrapper

import settings
from mocked import get_datasource_types, get_datasource_type


def fetch_annotations(conn, obj_dtype, obj_id):
    """
    Return the first available annotation for the given object in this app's
    namespace, or None if no annotation exists.
    """
    annotations = conn.getAnnotationLinks(
        obj_dtype, [obj_id], ns=settings.ANNOTATION_NAMESPACE)
    for annotation in annotations:
        yield annotation.getAnnotation()


def fetch_datasources(conn, obj_dtype, obj_id):
    for annotation in fetch_annotations(conn, obj_dtype, obj_id):
        datasource = json.loads(annotation.getValue())
        datasource["id"] = annotation.id
        yield datasource


def store_datasource(conn, obj_dtype, obj_id, datasource):
    obj = conn.getObject(str(obj_dtype), obj_id)
    TermAnnotationWrapper.createAndLink(
        obj, settings.ANNOTATION_NAMESPACE, val=datasource)


def remove_datasource(conn, obj_dtype, obj_id, datasource_id):
    handle = conn.deleteObjects('/Annotation', [datasource_id])
    try:
        conn._waitOnCmd(handle)
        return True
    finally:
        handle.close()


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
    try:
        bad = not remove_datasource(conn,  obj_dtype, obj_id, int(request.GET.get('datasource')))
        errs = 'Could not remove data source' if bad else None
    except Exception, ex:
        bad = True
        errs = str(ex)
    return dict(bad=bad, errs=errs)


@login_required()
@render_response()
def render_form(request, conn=None, **_kwargs):

    datasource_type = get_datasource_type(request.GET.get('datasource_type'))

    class Form(forms.Form):
        pass

    form = Form()

    for field in datasource_type['fields']:
        form.fields[field['name']] = forms.CharField(
            label=field['label'],
            initial=field['default'],
            required=field['required'],
            )

    context = {
        'form': form,
        'template': 'omero_external_data/datasource_type_form.html'
    }
    return context



                #{
                #    'name': 'url',
                #    'label': 'URL',
                #    'field_type': 'text',
                #    'default': None,
                #    'required': True,
                #},
