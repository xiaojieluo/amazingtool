from api.handler.APIHandler import APIHandler
import json

class index(APIHandler):
    def get(self):
        data = {
            'users':'/users/:username',
            'encode':{
                'md5':'/encode/md5',
            }
        }
        self.write_error(data, 404)
