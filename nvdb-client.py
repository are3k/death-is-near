from pprint import pprint

import numpy as np
import pandas as pd
from requests import get

api_base_url = "https://www.vegvesen.no/nvdb/api/v2/"


def get_json(base_url, endpoint):
    url = f"{base_url}{endpoint}.json"
    return get(url).json()


if __name__ == '__main__':
    # roadObjects = get_json(api_base_url, "vegobjekter")
    roadRefObjects = get_json(api_base_url, "vegobjekter/532")
    # pprint(roadRefObjects)

    for roadRefObject in roadRefObjects["objekter"]:
        roadRefFullObject = get_json(api_base_url, "vegobjekter/532/" + str(roadRefObject['id']))
        # pprint(roadRefFullObject)
        print(roadRefFullObject['lokasjon']['vegreferanser'][0]['kortform'])
