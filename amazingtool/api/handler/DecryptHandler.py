from api.handler.APIHandler import APIHandler
import hashlib


class index(APIHandler):
    '''
    解密 api,请求示例
    uri/decrypt?type='md5|sha256|sha512'&text=hello
    参数:
        type : 表示密文类型,有多个类型时, 使用 | 分割,当不确定类型时,可以留空
        text : 表示要加密的源数据
    '''

    # 该 api 支持的解密算法,过滤 type 参数用
    TYPE = ('md5', 'sha1','sha224','sha256','sha384','sha512', 'blake2b')

    def get(self):
        types = (self.get_argument('type', '|'.join(self.TYPE))).split('|')
        text = self.get_argument('text', '')
        result = dict()

        for type_ in types:
            result[type_] = self.decrypt(type_, text)

        data = dict(
            query = text,
            result = result
        )

        self.write_json(data)

    def decrypt(self, type_, text, charset='utf-8'):
        '''
        抽象的解密函数,利用 python 的反射机制,执行 hashlib 相应的加密函数,并更新加密数据库中的资料
        参数:
            type_ : 加密类型
            text : 需要加密的源数据
        '''
        if type_ in self.TYPE:
            return self.find(type_, {'text': text})
        else:
            return '暂不支持此算法'

    def find(self, type_, data):
        '''
        当数据不存在时,更新 mongodb 数据库
        查询加密数据库,当数据不存在时,返回提示字符
            type_ : 加密类型
            data  : 源数据与加密后的数据, dict 格式,
                { text:'', result:'' }
        '''
        db = self.db[type_]
        # 查询的时候要和 encrypt 反过来a查询,使用 result
        query = db.find_one({'result':data.get('text', '')})

        if query is None:
            return '数据库中没有数据,无法解密'
        else:
            return query.get('text')
