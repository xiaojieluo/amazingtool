from api.handler.APIHandler import APIHandler
import requests
import json
from api.model.isbn import isbn as ISBN
import tasks
import asyncio
import requests
import tornado

class index(APIHandler):
    def get(self):
        pass

class ip(APIHandler):
    '''
    ip 相关的 api 处理类
    '''
    # 数据返回类型
    TYPE = ('json', 'xml')

    @tornado.web.authenticated
    async def get(self, query):
        '''
        解析 查询参数
        '''
        # TODO: 如果查询 query 是 domain 的话,可以先解析成 ip,再在数据库中查找,数据库中不存在记录时才请求 ip-api
        #       因为 网络i/o 在网络状况不好时比较费时
        # TODO: 这里如果输入的 domain 带 http:// 或 https:// 时,需要去掉
        key = 'api.ip.{ip}'.format(ip=query)

        if self.cache.exists(key):
            data = self.cache.hgetall(key)
        else:
            data = self.find({'query': query}, 'ip')

        if data is None:
            data = await self.get_data(query)
            self.cache.hmset(key, data)
            await self.update(data, 'ip')

        self.write_json(data)

    async def get_data(self, query):
        url = 'http://ip-api.com/json/'+query
        r = requests.get(url)

        return json.loads(r.text)

class isbn(APIHandler):
    '''
    isbn 查询接口
    '''
    async def get(self, isbn):

        if len(isbn) == 13:
            isbn_type = 'isbn13'
        elif len(isbn) == 10:
            isbn_type = 'isbn10'
        else:
            self.write_error('isbn 错误')

        result = self.find({'isbn':isbn})
        if result is None:
                result = await self.get_data(isbn)

        self.write_json(result)

    async def get_data(self, isbn):
        url = 'https://api.douban.com/v2/book/isbn/'
        r = requests.get(url + isbn)
        print(r.text)
        if r.status_code == 200:
            tmp = json.loads(r.text)
            data = dict(
                title = tmp.get('title', ''),
                subtitle = tmp.get('subtitle', ''),
                author = tmp.get('author', ''),
                pubdate = tmp.get('pubdate', ''),
                image = tmp.get('image', ''),
                binding = tmp.get('binding', ''),
                isbn = isbn,
                isbn10 = tmp.get('isbn10', ''),
                isbn13 = tmp.get('isbn13', ''),
                translator = tmp.get('translator', ''),
                catalog = tmp.get('catalog', ''),
                pages = tmp.get('pages', ''),
                images = tmp.get('images', ''),
                publisher = tmp.get('publisher', ''),
                author_intro = tmp.get('author_intro', ''),
                summary = tmp.get('summary', ''),
            )
            result =  self.update({'isbn':isbn}, data)
            return result
        else:
            return json.loads(r.text)

class history(APIHandler):
    def get(self):
        month = self.get_argument('month', '01')
        day = self.get_argument('day', '01')

        cache_key = 'amazingtool.history.{month}.{day}'.format(month=month, day=day)

        if self.cache.exists(cache_key):
            history = self.cache.hgetall(cache_key)
            history['events'] = json.loads(history['events'].replace('\'', '"'))
        else:
            history = self.find({'day':day, 'month':month}, 'history')
            self.cache.hmset(cache_key, history)

        if history is None:
            self.write_error('error.')

        # 图片存储前缀 url
        img_url = 'http://or9eyjm3w.bkt.clouddn.com/'
        for his in history['events']:
            his['thumb'] = img_url + his['thumb']


        data = dict(
            result = history
        )
        self.write_json(data)
