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
        query = self.get_argument('query', '') # 查询参数
        type_ = self.get_argument('type', 'json')
        url = 'http://ip-api.com/json/'

        data = self.find({'query': query})
        if data is None:
            r = requests.get(url+query)
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
