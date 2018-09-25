from pprint import pprint

import requests
# from json import json

api = "https://www.vegvesen.no/nvdb/api/v2/"


# https://www.vegvesen.no/nvdb/api/v2/vegobjekter.json
def get_json(url, parameters, timeout):
    r = requests.get(url, params=parameters, timeout=timeout)
    r.raise_for_status()
    return r.json()


road_objects_json = get_json(api + 'vegobjekter.json', {}, 5)
pprint(road_objects_json)
