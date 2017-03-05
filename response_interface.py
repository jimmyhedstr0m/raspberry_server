import json


class Response():

    def succ_response(self, data):
        return json.dumps({"results": data}, indent=2, sort_keys=True, ensure_ascii=False)

    def err_response(self, data):
        return json.dumps({"error": data}, indent=2, sort_keys=True, ensure_ascii=False)
