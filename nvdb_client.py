
from pprint import pprint

import numpy as np
import pandas as pd
from requests import get

api_base_url = "https://www.vegvesen.no/nvdb/api/v2/"
default_numrows = 10000


def get_json(url):
    """Function to fetch API-data based on given URL. Returns dict or list"""
    # headers = {'X-Client': 'SSB Hackaton', 'X-Kontaktperson': 'egk@ssb.no'}
    print(url)
    return get(url).json()


def create_dataframe(data_dict):
    """Creates a Pandas dataframe from a dict"""
    data_frame = pd.DataFrame(data=data_dict)
    return data_frame


def create_vegref(fylke, kommune, kategori, status, nummer, hp):
    """Creates a modified vegreferanse kortnavn"""
    if fylke < 10:
        fylke = f"0{fylke}"
    if kommune < 10:
        kommune = f"0{kommune}"
    vegref = f"{fylke}{kommune} {kategori}{status.lower()}{nummer} hp{hp}"
    return vegref


def get_vegrefs():
    data = get_json(
        api_base_url + "vegobjekter/532?inkluder=lokasjon&egenskap=(4566=5493 OR 4566=5494 OR 4566=5492)&antall=" + str(
            default_numrows))
    # pprint(data)
    vegrefs = []
    while True:
        for vegref in data['objekter']:
            # print(vegref['lokasjon']['vegreferanser'][0]['kortform'])
            fylke = vegref['lokasjon']['vegreferanser'][0]['fylke']
            kommune = vegref['lokasjon']['vegreferanser'][0]['kommune']
            kategori = vegref['lokasjon']['vegreferanser'][0]['kategori']
            status = vegref['lokasjon']['vegreferanser'][0]['status']
            nummer = vegref['lokasjon']['vegreferanser'][0]['nummer']
            hp = vegref['lokasjon']['vegreferanser'][0]['hp']
            vegref_kort = create_vegref(fylke, kommune, kategori, status, nummer, hp)

            if vegref_kort not in vegrefs:
                vegrefs.append(vegref_kort)

        if data['metadata']['returnert'] == default_numrows:
            # print('ny side' + " etter " + str(data['metadata']['returnert']) + " treff")
            data = get_json(data['metadata']['neste']['href'])
        else:
            # print("det var " + str(data['metadata']['returnert']) + " treff på siste side")
            # print(len(data['objekter']))
            break
    return vegrefs


def get_fotobokser():
    fotoboks_data = get_json(api_base_url + "vegobjekter/775?inkluder=lokasjon&antall=" + str(default_numrows))
    print("Fotobokser")
    fotobokser = []
    while True:
        for fotoboks in fotoboks_data["objekter"]:
            if "vegreferanser" in fotoboks['lokasjon']:
                # print(fotoboks['lokasjon']['vegreferanser'][0]['kortform'])
                fylke = fotoboks['lokasjon']['vegreferanser'][0]['fylke']
                kommune = fotoboks['lokasjon']['vegreferanser'][0]['kommune']
                kategori = fotoboks['lokasjon']['vegreferanser'][0]['kategori']
                status = fotoboks['lokasjon']['vegreferanser'][0]['status']
                nummer = fotoboks['lokasjon']['vegreferanser'][0]['nummer']
                hp = fotoboks['lokasjon']['vegreferanser'][0]['hp']
                fotoboks_kort = create_vegref(fylke, kommune, kategori, status, nummer, hp)
                fotobokser.append(fotoboks_kort)

        if fotoboks_data['metadata']['returnert'] == default_numrows:
            # print('ny side' + " etter " + str(data['metadata']['returnert']) + " treff")
            fotoboks_data = get_json(fotoboks_data['metadata']['neste']['href'])
        else:
            # print("det var " + str(data['metadata']['returnert']) + " treff på siste side")
            # print(len(fotoboks_data['objekter']))
            break
    return fotobokser


if __name__ == '__main__':
    panda_dict = {}
    # vegrefs = get_vegrefs()
    # panda_dict["Vegreferanser"] = vegrefs
    fotobokser = [0] * 18549  # len(vegrefs)

    fotoboks_list = get_fotobokser()
    print(len(fotoboks_list))
