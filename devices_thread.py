import threading
import time
import requests
from auth_maas360 import auth
from endpoints import DEVICES_ENDPOINT


def fetch_devices_for_page(token, page_number, all_devices, query_params):
    """
    Essa função é responsável por buscar dispositivos de uma determinada página.

    Args:
    - token (str): Token de autorização para acessar a API.
    - page_number (int): Número da página a ser buscada.
    - all_devices (list): Lista que irá armazenar todos os dispositivos buscados.
    - query_params (dict): Parâmetros da query.

    Returns:
    None, a lista `all_devices` é modificada com os dispositivos encontrados.
    """
    query_params["pageNumber"] = page_number
    headers = {"Authorization": f'MaaS token="{token}"', "Accept": "application/json"}
    response = requests.get(DEVICES_ENDPOINT, params=query_params, headers=headers)
    devices = response.json()["devices"]["device"]
    all_devices.extend(devices)


def get_devices(token=auth()):
    """
    Essa função busca todos os dispositivos disponíveis.

    Args:
    - token (str): Token de autorização para acessar a API.

    Returns:
    - list: Lista com todos os dispositivos encontrados.
    """

    all_devices = []
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
    number_of_pages = (lambda x: int(x) if x.is_integer() else int(x) + 1)(
        count_total_devices / query_params["pageSize"]
    )
    threads = []
    for i in range(1, number_of_pages + 1):
        t = threading.Thread(
            target=fetch_devices_for_page, args=(token, i, all_devices, query_params)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return all_devices


if __name__ == "__main__":
    st = time.time()
    print(get_devices())
    et = time.time()
    print(f"tempo de execução: {et - st}")
