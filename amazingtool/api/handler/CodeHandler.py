from api.handler.APIHandler import APIHandler
import asyncio
import tornado
import hashlib
import tasks
import api.web
import base64

class index(APIHandler):
    def get(self):
        pass


encrypt_key = 'api.encrypt.{text}'
decrypt_key = 'api.decrypt.{text}'

class encrypt(APIHandler):
    '''
    加密 api,请求示例
    uri/encrypt?type='md5|sha256|sha512'&text=hello
    参数:
        type : 表示加密类型,当类型有多个时, 使用 | 分割
        text : 表示要加密的源数据
    '''

    # 该 api 支持的加密算法,过滤 type 参数用
    TYPE = ('md5', 'sha1','sha224','sha256','sha384','sha512', 'blake2b')

    @tornado.web.authenticated
    async def get(self, text):
        # 不指定 type, 则返回所有类型的加密数据
        types = (self.get_argument('type', '|'.join(self.TYPE))).split('|')
        result = dict()

        for type_ in types:
            if type_ in self.TYPE:
                tmp = self.cache.exists(encrypt_key.format(text=text))
                # print(encrypt_key.format(text=text))

                if tmp and self.cache.hexists(encrypt_key.format(text=text), type_):
                    cache = self.cache.hget(encrypt_key.format(text=text), type_)
                    # print(cache)
                    result[type_] = bytes.decode(cache)
                else:
                    result[type_] = await self.encrypt(type_, text)
                    await self.update_cache(type_, {'text': text, 'result': result})

            else:
                return 'The encryption algorithm is not supported at this time'

        data = dict(query = text,result = result)

        self.write_json(data)

    async def encrypt(self, type_, text, charset='utf-8'):
        '''
        抽象的加密函数,利用 python 的反射机制,执行 hashlib 相应的加密函数,并更新加密数据库中的资料
        参数:
            type_ : 加密类型
            text : 需要加密的源数据
        '''
        if hasattr(hashlib, type_):
            result =  getattr(hashlib, type_)(text.encode(charset)).hexdigest()
            return result


    async def update_cache(self, type_, data):
        '''
        異布更新緩存與數據庫
        '''
        text = data.get('text', '')
        print(data)
        result = data.get('result', '')

        # if self.cache.exists(encrypt_key.format(text=text)) is False:
            # print("不存在， 更新數據")
        self.cache.hmset(encrypt_key.format(text=text), {type_:result[type_]})
        # Redis 中沒有緩存時將數據丟給 celery 去更新数据库
        tasks.update.delay(type_, data)
        self.cache.hmset(decrypt_key.format(text=result[type_]), {type_:text})


class decrypt(APIHandler):
        '''
        解密 api,请求示例
        uri/decrypt?type='md5|sha256|sha512'&text=hello
        参数:
            type : 表示密文类型,有多个类型时, 使用 | 分割,当不确定类型时,可以留空
            text : 表示要加密的源数据
        '''

        # 该 api 支持的解密算法,过滤 type 参数用
        TYPE = ('md5', 'sha1','sha224','sha256','sha384','sha512', 'blake2b')

        async def get(self, text):
            types = (self.get_argument('type', '|'.join(self.TYPE))).split('|')
            result = dict()

            for type_ in types:
                if type_ in self.TYPE:

                    if self.cache.hexists(decrypt_key.format(text=text), type_):
                        # 命中緩存
                        cache = self.cache.hget(decrypt_key.format(text=text), type_)
                        result[type_] = bytes.decode(cache)
                    else:
                        # print(type_)

                        result[type_] = await self.decrypt(type_, text)
                else:
                    result[type_] = 'The encryption algorithm is not supported at this time'

            data = dict(
                query = text,
                result = result
            )

            self.write_json(data)

        async def decrypt(self, type_, text, charset='utf-8'):
            '''
            抽象的解密函数,利用 python 的反射机制,执行 hashlib 相应的加密函数,并更新加密数据库中的资料
            参数:
                type_ : 加密类型
                text : 需要加密的源数据
            '''
            # if type_ in self.TYPE:
            # key = 'api.decrypt.{query}'.format(query=text)
            result =  self.find({'result':text}, type_)
            if result:
                return result
        #
        # def find(self, type_, data):
        #     '''
        #     当数据不存在时,更新 mongodb 数据库
        #     查询加密数据库,当数据不存在时,返回提示字符
        #         type_ : 加密类型
        #         data  : 源数据与加密后的数据, dict 格式,
        #             { text:'', result:'' }
        #     '''
        #     db = self.db[type_]
        #     # 查询的时候要和 encrypt 反过来a查询,使用 result
        #     query = db.find_one({'result':data.get('text', '')})
        #
        #     if query is None:
        #         return '数据库中没有数据,无法解密'
        #     else:
        #         return query.get('text')

class encode(APIHandler):
    '''
    加密 api,请求示例
    uri/encrypt?type=base64&text=hello
    参数:
        type : 表示加密类型,当类型有多个时, 使用 | 分割
        text : 表示要加密的源数据
    '''

    # 该 api 支持的加密算法,过滤 type 参数用
    TYPE = ('base16','base32', 'base64', 'base85')

    async def get(self, text):
        types = (self.get_argument('type', '|'.join(self.TYPE))).split('|')
        result = dict()

        for type_ in types:
            if type_ in self.TYPE:
                result[type_] = await self.encode(type_, text)
            else:
                result[type_] = 'The encryption algorithm is no  t supported at this time'

        data = dict(
            query = text,
            result = result
        )

        self.write_json(data)

    async def encode(self, type_, text, charset='utf-8'):
        '''
        抽象的编码函数,利用 python 的反射机制,执行 base64 相应的加密函数,并更新 编码 数据库中的资料
        参数:
            type_ : 编码类型
            text : 需要编码的源数据
        '''

        # 组合 base 编码名称,转换成 base64 库 需要的格式
        types = (type_[0:1]+type_[-2:]+'encode')

        if hasattr(base64, types):
            result = getattr(base64, types)(text.encode()).decode()
            return result
