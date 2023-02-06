import requests
from auth_maas360 import auth
from endpoints import DEVICES_ENDPOINT


class DeviceRequestHandler(object):
    def __init__(self, token):
        self.session = requests.Session()
        self.token = token
        self.session.headers.update(
            {
                "Authorization": f'MaaS token="{self.token}"',
                "Accept": "application/json",
            }
        )

    def get(self, url, query_params={}):
        response = self.session.get(url, params=query_params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def close(self):
        self.session.close()


if __name__ == "__main__":
    url = DEVICES_ENDPOINT
    query_params = {
        "match": 0,
        "operator": "AND",
        "pageNumber": 1,
        "pageSize": 50,
        "sortAttribute": "lastreported",
        "sortOrder": "dsc",
    }
