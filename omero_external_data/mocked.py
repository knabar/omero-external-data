import json


class DataSource(object):
    
    def render(self):
        return "Hello World"

    @property
    def label(self):
        return "External Data"


DATASOURCE_TYPES = [
        {
            'name': 'youtube',
            'label': 'Youtube video',
            'driver': 'omero_external_data.drivers.youtube',
            'fields': [
                {
                    'name': 'url',
                    'label': 'URL',
                    'field_type': 'text',
                    'default': None,
                    'required': True,
                },
            ],
        },
    ]


def get_datasource_types(object_dtype):
    return DATASOURCE_TYPES

def get_datasource_type(datasource_type):
    for ds_type in DATASOURCE_TYPES:
        if ds_type['name'] == datasource_type:
            return ds_type
    return None

