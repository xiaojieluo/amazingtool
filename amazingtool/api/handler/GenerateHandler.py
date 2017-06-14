from api.handler.APIHandler import APIHandler
import asyncio

class index(APIHandler):
    def get(self):
        pass

class verificate_code(APIHandler):
    def get(self, code):
        print(code)
        pass
