from api.handler.APIHandler import APIHandler
import base64


class index(APIHandler):
    '''
    加密 api,请求示例
    uri/encrypt?type=base64&text=hello
    参数:
        type : 表示加密类型,当类型有多个时, 使用 | 分割
        text : 表示要加密的源数据
    '''

    # 该 api 支持的加密算法,过滤 type 参数用
    TYPE = ('base16','base32', 'base64', 'base85')

    def get(self):
        types = (self.get_argument('type', '')).split('|')
        text = self.get_argument('text', '')
        data = dict()

        for type_ in types:
            data[type_] = self.encode(type_, text)

        self.write_json(data)

    def encode(self, type_, text, charset='utf-8'):
        '''
        抽象的编码函数,利用 python 的反射机制,执行 base64 相应的加密函数,并更新 编码 数据库中的资料
        参数:
            type_ : 编码类型
            text : 需要编码的源数据
        '''
        # types =

        # 组合 base 编码名称,转换成 base64 库 需要的格式
        # for k in self.TYPE:
        #     types.append(k[0:1]+k[-2:]+'encode')
        types = (type_[0:1]+type_[-2:]+'encode')

        # print(types)
        if type_ in self.TYPE:
            print("in")
            if hasattr(base64, types):
                print("has")
                result = getattr(base64, types)(text.encode()).decode()
                self.update(type_, {'text': text, 'result': result})
                return result
            pass
        else:
            return 'The encryption algorithm is no  t supported at this time'



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
