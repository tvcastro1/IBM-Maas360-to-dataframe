from dataclasses import dataclass, field
from typing import Optional
from auth_maas360 import auth
from endpoints import DEVICES_ENDPOINT
import requests
from threading import Thread


@dataclass
class Devices:
    token: str = auth()
    all_devices: list = field(default_factory=list)
    query_params: Optional[dict] = {
        "match": 0,
        "operator": "AND",
        "pageNumber": 1,
        "pageSize": 50,
        "sortAttribute": "lastreported",
        "sortOrder": "dsc",
    }
    headers: Optional[dict] = {
        "Authorization": f'MaaS token="{token}"',
        "Accept": "application/json",
    }
    url: str = DEVICES_ENDPOINT

    def fetch_devices_for_page(self, page_number):
        self.query_params["pageNumber"] = page_number
        response = requests.get(
            self.url, params=self.query_params, headers=self.headers
        )
        devices = response.json()["devices"]["device"]
        self.all_devices.extend(devices)


def get_devices(self):
    response = requests.get(self.url, params=self.query_params, headers=self.headers)
    count_total_devices = response.json()["devices"]["count"]
    number_of_pages = (lambda x: int(x) if x.is_integer() else int(x) + 1)(
        count_total_devices / self.query_params["pageSize"]
    )
    threads = []
    for i in range(1, number_of_pages + 1):
        t = Thread(target=self.fetch_devices_for_page, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return self.all_devices


if __name__ == "__main__":
    devices = Devices()
