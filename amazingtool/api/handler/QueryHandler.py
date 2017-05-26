from api.handler.APIHandler import APIHandler
import requests
import json

class index(APIHandler):
    def get(self):
        pass

class isbn(APIHandler):
    '''
    isbn 查询接口
    '''
    def get(self):
        isbn = self.get_argument('isbn', '')

        if len(isbn) == 13:
            isbn_type = 'isbn13'
        elif len(isbn) == 10:
            isbn_type = 'isbn10'
        else:
            self.write_error('isbn 错误')

        result = self.find({'isbn':isbn})
        # print(result)
        if result is None:
            url = 'https://api.douban.com/v2/book/isbn/'
            r = requests.get(url + isbn)
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
            else:
                self.write_error()

        self.log("query isbn "+ isbn)
        self.write_json(result)

    def find(self, data, type_='isbn', projection=dict(_id=False, isbn=False)):
        '''
        由于网络请求比较慢,所以先查询本地数据库,
        当本地数据库没有记录的时候,再通过 外部api 请求
        '''
        db = self.db[type_]
        result = db.find_one({'isbn':data.get('isbn', '')}, projection)
        return result

    def update(self, query, data, type_='isbn'):
        '''
        当数据不存在时,更新 mongodb 数据库
            type_ : 类型
            data  : 要写入数据库的内容, dict 格式,
                { text:'', result:'' }
        '''
        db = self.db[type_]
        if db.find_one(query) is None:
            db.insert_one(data)

        return self.find(query)
