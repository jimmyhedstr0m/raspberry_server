import json


class Response():

    def succ_response(self, data):
        return {"results": data}

    def err_response(self, data):
        return {"error": data}
