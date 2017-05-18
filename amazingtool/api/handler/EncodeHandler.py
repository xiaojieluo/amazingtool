from api.handler.APIHandler import APIHandler
import hashlib

class md5(APIHandler):
    '''
    md5 加密
    '''
    def get(self):
        query = self.get_query_argument('query', '')
        result = hashlib.md5(query.encode('utf-8')).hexdigest()

        data = {
            'query': query,
            'result': result
        }

        if self.db.md5.find_one({'query':query}) is None:
            self.db.md5.insert_one({'query':query,'result':result})

        self.write_json(data)
