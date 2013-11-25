import json

from django.http import Http404, HttpResponse
from django import forms

from omeroweb.webclient.decorators import login_required, render_response
from omero.gateway import TermAnnotationWrapper

from omero.ds.core import DataSource


@login_required()
@render_response()
def index(request, obj_dtype, obj_id, conn=None, **_kwargs):

    template = "omero_external_data/omero_external_data.html"
    error = ""

    if request.method == 'POST':

        if request.GET.has_key('add_datasource'):

            datasource_type = next(
                dstype for dstype in conn.listDatasourceTypes(obj_dtype)
                if dstype.ds_name == request.POST.get('datasource_type')
                )

            form = generate_form(datasource_type, request.POST)

            if form.is_valid():

                datasource = DataSource({
                    'name': form.cleaned_data['name'],
                    'label': form.cleaned_data['label'],
                    'type': request.POST.get('datasource_type'),
                    'inputs': [
                        {
                            'name': field['name'],
                            'value': form.cleaned_data[field['name']],
                        }
                        for field in datasource_type['inputs']
                    ],
                })
                conn.attachDatasource(datasource, obj_dtype, obj_id)

            else:

                return dict(bad=True, errs=form.errors)

    datasources = conn.listDatasources(obj_dtype, obj_id)

    datasource_types = conn.listDatasourceTypes(obj_dtype)

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
    result = conn.openDatasourceCursor(int(request.GET.get('datasource'))).read()
    return HttpResponse(content=result)


@login_required()
@render_response()
def delete_datasource(request, obj_dtype, obj_id, conn=None, **_kwargs):
    try:
        bad = not conn.removeDatasource(request.GET.get('datasource'))
        errs = 'Could not remove data source' if bad else None
    except Exception, ex:
        bad = True
        errs = str(ex)
    return dict(bad=bad, errs=errs)


def generate_form(datasource_type, form_data=None):

    class Form(forms.Form):
        name = forms.CharField(label='Name', required=True)
        label = forms.CharField(label='Label', required=True)

    form = Form(form_data)

    for field in datasource_type['inputs']:
        form.fields[field['name']] = forms.CharField(
            label=field['label'],
            initial=field['default'],
            required=field['required'],
            )

    return form


@login_required()
@render_response()
def render_form(request, obj_dtype, obj_id, conn=None, **_kwargs):

    datasource_type = next(
        dstype for dstype in conn.listDatasourceTypes(obj_dtype)
        if dstype.ds_name == request.GET.get('datasource_type')
        )

    form = generate_form(datasource_type)

    context = {
        'form': form,
        'template': 'omero_external_data/datasource_type_form.html'
    }
    return context
