from api.handler.APIHandler import APIHandler
import hashlib


class index(APIHandler):
    '''
    加密 api,请求示例
    uri/encode?type='md5|sha256|sha512'&text=hello
    参数:
        type : 表示加密类型,当类型有多个时, 使用 | 分割
        text : 表示要加密的源数据
    '''

    def get(self):
        types = (self.get_argument('type', '')).split('|')
        text = self.get_argument('text', '')
        data = dict()

        for type_ in types:
            data[type_] = self.encode(type_, text)

        self.write_json(data)

    def encode(self, type_, text, charset='utf-8'):
        '''
        抽象的加密函数,利用 python 的反射机制,执行 hashlib 相应的加密函数,并更新加密数据库中的资料
        参数:
            type_ : 加密类型
            text : 需要加密的源数据
        '''
        if type_ in ['md5', 'sha1','sha224','sha256','sha384','sha512', 'blake2b']:
            if hasattr(hashlib, type_):
                result =  getattr(hashlib, type_)(text.encode(charset)).hexdigest()
                self.update(type_, {'text': text, 'result': result})

                return result

    def update(self, type_, data):
        '''
        当数据不存在时,更新 mongodb 数据库
            type_ : 加密类型
            data  : 源数据与加密后的数据, dict 格式,
                { text:'', result:'' }
        '''
        db = self.db[type_]
        if db.find_one({'text':data.get('text', '')}) is None:
            db.insert_one({'text': data.get('text', ''), 'result': data.get('result', '')})
