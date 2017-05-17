#!/usr/bin/env python
# coding=utf-8

from api.handler.APIHandler import APIHandler

class index(APIHandler):
    def get(self, username):
        data = {
            "name":username
        }
        self.write_json(data)
