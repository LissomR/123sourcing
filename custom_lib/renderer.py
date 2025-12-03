from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class JSONResponseRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'errorCode': 0,
            'errorMessage': 'Success',
            "data":[]
        }
        if data:
            response_dict['data']=data
        data = response_dict
        return json.dumps(data,default=str)
