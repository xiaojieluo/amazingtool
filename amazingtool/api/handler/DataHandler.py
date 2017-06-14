from api.handler.APIHandler import APIHandler
import json
import pickle


class gdp(APIHandler):

    def get(self):
        year = self.get_argument('year', '')

        key = 'api.data.gdp.{year}'.format(year=year)

        if self.cache.exists(key):
            data = self.cache.hgetall(key)
            data['gdp'] = json.loads(data['gdp'].replace('\'', '"'))
        else:
            data = self.find({'year':year}, 'gdp')

        if data:
            self.cache.hmset(key, data)
            self.write_json(data)
        else:
            self.write_error('data cannot find')
