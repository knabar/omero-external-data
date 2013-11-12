import json


class DataSource(object):
    
    def render(self):
        return "Hello World"

    @property
    def label(self):
        return "External Data"



def get_datasource_types(object_dtype):
    
    #name
    #label
    #driver
    #required_field = {
    #    name
    #    label
    #    field_type
    #    default
    #}
    
    return [
        {
            'name': 'youtube',
            'label': 'Youtube video',
        },
        {
            'name': 'hdf5',
            'label': 'HDF5',
        },
    ]


