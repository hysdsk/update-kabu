from configparser import ConfigParser
import os
import requests

class KabusAPI(object):
    def __init__(self):
        config = ConfigParser()
        config.read("config.ini")
        host = config["kabusapi"]["host"]
        port = config["kabusapi"]["port"]
        self.url = f"http://{host}:{port}/kabusapi"
        self.headers = { "Host": "localhost" }
        token = self._gettoken(os.getenv("KABUS_PASSWORD"))
        self.headers.update({"X-API-KEY": token})

    def _gettoken(self, password):
        post = { "APIPassword": password }
        res = requests.post(f"{self.url}/token", headers=self.headers, json=post)
        if 200 == res.status_code:
            return res.json()["Token"]
        else:
            print(f"Failed to get token. status: {res.status_code}")
            return None

    def get_symbol(self, code, exchange):
        res = requests.get(f"{self.url}/symbol/{code}@{exchange}", headers=self.headers)
        if 200 == res.status_code:
            return res.json()
        else:
            print(f"Failed to get symbol. Symbol: {code}@{exchange} Response: {res.json()}")
            return None

    def put_unregister(self, code, exchange):
        put = { "Symbols": [{ "Symbol": code, "Exchange": exchange }]}
        res = requests.put(f"{self.url}/unregister", headers=self.headers, json=put)
        if 200 != res.status_code:
            print(f"Failed to put unregister. Symbol: {code}@{exchange} Response: {res.json()}")
