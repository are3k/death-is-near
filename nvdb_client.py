
from pprint import pprint

import numpy as np
import pandas as pd
from requests import get

api_base_url = "https://www.vegvesen.no/nvdb/api/v2/"
default_numrows = 10000


def get_json(url):
    """Function to fetch API-data based on given URL. Returns dict or list"""
    #headers = {'X-Client': 'SSB Hackaton', 'X-Kontaktperson': 'egk@ssb.no'}
    print(url)
    return get(url).json()




if __name__ == '__main__':
    data = get_json(api_base_url + "vegobjekter/532?inkluder=lokasjon&egenskap=(4566=5493 OR 4566=5494 OR 4566=5492)&antall=" + str(default_numrows))
    #pprint(data)
    while True:
        for vegref in data['objekter']:
            print(vegref['lokasjon']['vegreferanser'][0]['kortform'])
        if data['metadata']['returnert'] == default_numrows:
            print('ny side' + " etter " + str(data['metadata']['returnert']) + " treff")
            data = get_json(data['metadata']['neste']['href'])
        else:
            print("det var " + str(data['metadata']['returnert']) + " treff på siste side")
            print(len(data['objekter']))
            break