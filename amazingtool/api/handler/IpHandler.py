from api.handler.APIHandler import APIHandler
import requests
import json

class index(APIHandler):
    '''
    ip 相关的 api 处理类
    '''
    # 数据返回类型
    TYPE = ('json', 'xml')

    def get(self):
        '''
        解析 查询参数
        '''
        # TODO: 如果查询 query 是 domain 的话,可以先解析成 ip,再在数据库中查找,数据库中不存在记录时才请求 ip-api
        #       因为 网络i/o 在网络状况不好时比较费时
        # TODO: 这里如果输入的 domain 带 http:// 或 https:// 时,需要去掉
        query = self.get_argument('query', '') # 查询参数
        type_ = self.get_argument('type', 'json')
        url = 'http://ip-api.com/json/'

        data = self.find({'query': query})
        if data is None:
            r = requests.get(url+query)
            # TODO: 发送异步任务到 celery, 请求 ip-api 数据库,获取 ip的最新数据,与本地数据库比较
            # 若比本地数据库新,则替换本地数据库
            data = self.update('ip', json.loads(r.text))

        self.write_json(data)

    def find(self, data, type_='ip'):
        '''
        由于网络请求比较慢,所以先查询本地数据库,
        当本地数据库没有记录的时候,再通过 外部api 请求
        '''
        db = self.db[type_]
        result = db.find_one({'query':data.get('query', '')}, {'_id':False})

        return result

    def update(self, type_, data):
        '''
        当数据不存在时,更新 mongodb 数据库
            type_ : 类型
            data  : 要写入数据库的内容, dict 格式,
                { text:'', result:'' }
        '''
        db = self.db[type_]
        if db.find_one({'query':data.get('query', '')}) is None:
            db.insert_one(data)

        return self.find(data)
