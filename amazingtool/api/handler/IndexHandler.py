from api.handler.APIHandler import APIHandler
import json

class index(APIHandler):
    def get(self):
        data = {
            'users':'/users/:username',
            'encrypt':self.site_url('encrypt/helloworld?type=md5|sha1|sha224|sha256|sha384|sha512|base64'),
            'decode':{
                'md5':self.site_url('decrypt/md5'),
            },
            'decode':self.site_url('decrypt/fc5e038d38a57032085441e7fe7010b0?type=base64|md5|sha1|sha224|sha256|sha384|sha512'),
            'query':{
                'ip':self.site_url('ip/1.1.1.1'),
                'history':self.site_url('history')
            }
        }
        self.write_json(data)
