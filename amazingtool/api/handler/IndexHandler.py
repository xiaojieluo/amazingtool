from api.handler.APIHandler import APIHandler
import json

class index(APIHandler):
    def get(self):
        data = {
            'users':'/users/:username',
            'encode':{
                'md5':self.site_url('encode/md5'),
                'sha1':self.site_url('/encode/sha1'),
                'sha224':self.site_url('/encode/sha224'),
                'sha256':self.site_url('/encode/sha256'),
                'sha384':self.site_url('/encode/sha384'),
                'sha512':self.site_url('encode/sha512'),
            },
            'decode':{
                'md5':self.site_url('decode/md5'),
            }
        }
        self.write_json(data)
