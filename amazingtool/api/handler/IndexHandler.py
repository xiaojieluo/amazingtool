from api.handler.APIHandler import APIHandler

class index(APIHandler):
    def get(self):
        data = {
            'users':'/users/:username'
        }
        self.write("Hello")
        # self.write_error(data, 404)
