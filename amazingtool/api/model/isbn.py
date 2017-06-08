from amazingtool.db import db

class isbn(object):

    def __init__(self):
        self.db = db

    def find(self, data, type_='isbn', projection=dict(_id=False, isbn=False)):
        '''
        由于网络请求比较慢,所以先查询本地数据库,
        当本地数据库没有记录的时候,再通过 外部api 请求
        '''
        database = self.db[type_]
        result = database.find_one(data, projection)
        return result

    def update(self, query, data, type_='isbn'):
        '''
        当数据不存在时,更新 mongodb 数据库
            type_ : 类型
            data  : 要写入数据库的内容, dict 格式,
                { text:'', result:'' }
        '''
        database = self.db[type_]
        if database.find_one(query) is None:
            database.insert_one(data)

        return self.find(query)
