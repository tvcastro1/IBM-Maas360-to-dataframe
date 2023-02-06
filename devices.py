import requests
from auth_maas360 import auth
from endpoints import DEVICES_ENDPOINT
import time


def get_devices(token):
    all_devices = []

    """
    Make a GET request to the DEVICES_ENDPOINT with the provided `token`.

    Args:
    - token (str): The token used for authentication.

    Returns:
    - requests.Response: The response from the GET request.
    """
    query_params = {
        "match": 0,
        "operator": "AND",
        "pageNumber": 1,
        "pageSize": 50,
        "sortAttribute": "lastreported",
        "sortOrder": "dsc",
    }
    headers = {"Authorization": f'MaaS token="{token}"', "Accept": "application/json"}
    response = requests.get(DEVICES_ENDPOINT, params=query_params, headers=headers)
    count_total_devices = response.json()["devices"]["count"]
    devices = response.json()["devices"]["device"]
    all_devices.extend(devices)
    number_of_pages = (lambda x: int(x) if x.is_integer() else int(x) + 1)(
        count_total_devices / query_params["pageSize"]
    )

    current_page = 2
    query_params["pageNumber"] = current_page

    while current_page <= number_of_pages:
        response = requests.get(DEVICES_ENDPOINT, params=query_params, headers=headers)
        devices = response.json()["devices"]["device"]
        all_devices.extend(devices)
        current_page += 1
        query_params["pageNumber"] = current_page
    return all_devices


"""     while True:
        query_params["pageNumber"] = page_number
        response = requests.get(DEVICES_ENDPOINT, params=query_params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            devices.extend(data["devices"]["device"])

            # Check if there are more pages
            if len(devices) > 0:
                print("tá indo o loop") """

# print(json.dumps(response.json(), indent=2))
# with open("json.txt", "w") as f:
# f.write(json.dumps(response.json(), indent=1))


if __name__ == "__main__":
    st = time.time()
    auth_token = auth()
    print(get_devices(auth_token))
    et = time.time()
    print(f"tempo de execução: {et - st}")
