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

        data = self.find({'query': query}, 'ip')
        if data is None:
            # r = requests.get(url+query)
            ip_data = await self.get_data(query)
            # result = tasks.ip.delay(query)
            # ip_data = result.get()
            # TODO: 发送异步任务到 celery, 请求 ip-api 数据库,获取 ip的最新数据,与本地数据库比较
            # 若比本地数据库新,则替换本地数据库
            # data = self.update('ip', json.loads(r.text))
            data = await self.update(ip_data, 'ip')
            self.write_error("暂无数据,已加入抓取队列")
        self.write_json(data)

    async def get_data(self, query):
        url = 'http://ip-api.com/json/'
        r = requests.get(url+query)

        return json.loads(r.text)

    # def update(self, type_, data):
    #     '''
    #     当数据不存在时,更新 mongodb 数据库
    #         type_ : 类型
    #         data  : 要写入数据库的内容, dict 格式,
    #             { text:'', result:'' }
    #     '''
    #     db = self.db[type_]
    #     if db.find_one({'query':data.get('query', '')}) is None:
    #         db.insert_one(data)
    #
    #     return self.find(data)

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



class weather(APIHandler):
    '''
    天气接口
    '''
    def get(self, city):

        if city == '':city = 'china'
        url = 'http://flash.weather.com.cn/wmaps/xml/{city}.xml'

        r = requests.get(url.format(city=city))
        r.encoding = 'unicode'
        import xmltodict
        data =json.dumps(xmltodict.parse(r.text))

        print(data.encode('gb2312'))
        # import pprint
        # pprint.pprint(data['china'])

        print(city)
        pass
