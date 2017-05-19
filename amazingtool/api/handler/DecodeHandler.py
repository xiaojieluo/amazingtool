from api.handler.APIHandler import APIHandler
import hashlib

class md5(APIHandler):
    '''
    md5 加密
    '''
    def get(self):
        text = self.get_query_argument('text', '')

        # if self.db.md5.find_one({'text':text}) is None:
        #     result = self.db.md5.insert_one({'text':text,'result':result})

        result = self.db.md5.find_one({'text':text})
        print(result)

        # data = dict(
        #     text = text,
        #     result =
        # )
        # self.write_json(data)
