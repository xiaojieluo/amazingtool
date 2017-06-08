
from pymongo import MongoClient


class database(object):

    def __init__(self, url='localhost', port=27017, database='amazingtool'):
        self.client = MongoClient(url, port)[database]
        # self.db = client[database]

db = database()


# import motor.motor_tornado
# import tornado
# import tornado.web
# from tornado.ioloop import IOLoop
# import time
#
# class database(object):
#
#     def __init__(self, url='localhost', port=27017, database='amazingtool'):
#         self.client = motor.motor_tornado.MotorClient(url, port)[database]
#
# db = database().client
#
# print(db)


#     def collection(self, collection):
#         return self.client[collection]
#
# class Ip(Database):
#
#     collection = 'ip'
#
#     def __init__(self):
#         super().__init__()
#         self.db = super().collection(self.collection)
#
#     def update(self):
#         pass
#
#     @tornado.web.asynchronous
#     @tornado.gen.coroutine
#     def finds(self):
#         feature = yield self.db.find({})
#         return feature

    # def __getattr__(self, name):
    #     pass


# ip = Ip()
# print(ip.finds())

# class Db(object):
#
#     def __init__(self, database='amazingtool'):
#         self.db = Database()[database]

    # def __init__(self, url='localhost', port=27017, database='amazingtool'):
    #     # client = motor.motor_tornado.MotorClient(url, port)
    #     # self.db = [database]
    #     super().__init__(url, port)
    #     # self.tests.find()
    #     self.db =
    #     pass

    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    # def do_insert(self):
    #     for i in range(0, 100):
    #         future = yield self.test_collection.insert_one({'i':i})
    #         return future

# db = Database()


# IOLoop.current().run_sync(db.do_insert)
# print(db.do_insert())
# db.do_insert()

# def test():
#     test = db.test
#     print(help(test['test']))
#     # msg = yield db.test.insert_one({'i':1})
#     # return msg
#
# # print(test())
# test()
