from api.handler.APIHandler import APIHandler
import hashlib

class md5(APIHandler):
    '''
    md5 加密
    '''
    def get(self):
        text = self.get_query_argument('text', '')
        result = hashlib.md5(text.encode('utf-8')).hexdigest()

        data = {
            'text': text,
            'result': result
        }

        if self.db.md5.find_one({'text':text}) is None:
            self.db.md5.insert_one({'text':text,'result':result})

        self.write_json(data)

class sha256(APIHandler):
    '''
    sha256 加密
    '''
    def get(self):
        text = self.get_query_argument('text', '')
        result = hashlib.sha256(text.encode('utf-8')).hexdigest()

        data = dict(
            text = text,
            result = result
        )

        if self.db.sha256.find_one({'text':text}) is None:
            self.db.sha256.insert_one({'text':text,'result':result})

        self.write_json(data)

class sha224(APIHandler):
    '''
    sha224 加密
    '''
    def get(self):
        text = self.get_query_argument('text', '')
        result = hashlib.sha224(text.encode('utf-8')).hexdigest()

        data = dict(
            text = text,
            result = result
        )

        if self.db.sha224.find_one({'text':text}) is None:
            self.db.sha224.insert_one({'text':text, 'result':result})

        self.write_json(data)
