import re
import os
from pathlib import Path
from pprint import pprint

import numpy as np
import pandas as pd
from requests import get

VEI_REF_MAL = re.compile(r'(.+) m.*')

api_base_url = "https://www.vegvesen.no/nvdb/api/v2/"
default_numrows = 10000


def get_json(url):
    """Function to fetch API-data based on given URL. Returns dict or list"""
    # headers = {'X-Client': 'SSB Hackaton', 'X-Kontaktperson': 'egk@ssb.no'}
    print(url)
    return get(url).json()


def get_vei_referanser(data, vei_referanser_file):
    vei_dict = dict()

    with open(vei_referanser_file, 'w') as f:
        while True:
            for vegref in data['objekter']:
                kortform = vegref['lokasjon']['vegreferanser'][0]['kortform']
                kortform_uten_meter_suffix = VEI_REF_MAL.match(kortform).group(1)
                if kortform_uten_meter_suffix not in vei_dict:
                    print(kortform_uten_meter_suffix)
                    vei_dict[kortform_uten_meter_suffix] = None
                    f.write(kortform_uten_meter_suffix + "\n")
            if data['metadata']['returnert'] == default_numrows:
                print('ny side' + " etter " + str(data['metadata']['returnert']) + " treff")
                data = get_json(data['metadata']['neste']['href'])
            else:
                print("det var " + str(data['metadata']['returnert']) + " treff på siste side")
                print(len(data['objekter']))
                break

    return vei_dict


def match_vei_referanser(data, vei_ref_dict):
    while True:
        for fartsdemper in data['objekter']:
            if 'vegreferanser' in fartsdemper['lokasjon']:
                # ta bare de fartsdempere på ikke-kommunale veier
                if fartsdemper['lokasjon']['vegreferanser'][0]['kommune'] == 0:
                    vei_referanse_til_objektet = fartsdemper['lokasjon']['vegreferanser'][0]['kortform']
                    vei_referanse_til_objektet_uten_meter_suffix = VEI_REF_MAL.match(vei_referanse_til_objektet).group(1)
                    if vei_referanse_til_objektet_uten_meter_suffix in vei_ref_dict:
                        vei_ref_dict[vei_referanse_til_objektet_uten_meter_suffix] = 1
                    else:
                        print('vei referanse {} fra fartsdemper {} finnes ikke i vei referanse lista'
                              .format(vei_referanse_til_objektet_uten_meter_suffix,
                                      fartsdemper['id']))
            else:
                print('fartsdemper id {} har ikke vei referanse'.format(fartsdemper['id']))
        if data['metadata']['returnert'] == default_numrows:
            print('ny side' + " etter " + str(data['metadata']['returnert']) + " treff")
            data = get_json(data['metadata']['neste']['href'])
        else:
            print("det var " + str(data['metadata']['returnert']) + " treff på siste side")
            print(len(data['objekter']))
            break


def les_vei_referanser_fra_fil(vei_dict):
    with open('vei_referanser.txt', 'r') as f:
        for line in f:
            line_without_newline = line.replace("\n", "")
            vei_dict[line_without_newline] = None


if __name__ == '__main__':
    europavegId = '5492'
    riksvegId = '5493'
    fylkesvegId = '5494'

    vei_referanser_file = Path("vei_referanser.txt")
    veg_dict = dict()

    if vei_referanser_file.exists() and os.path.getsize(vei_referanser_file) > 0:
        les_vei_referanser_fra_fil(veg_dict)
    else:
        vei_referanse_ider = get_json(api_base_url + "vegobjekter/532?"
                                                     "inkluder=lokasjon"
                                                     "&egenskap=("
                                                     "{veiKategoriId}={riksveg} "
                                                     "OR {veiKategoriId}={fylkesveg} "
                                                     "OR {veiKategoriId}={europaveg})"
                                      .format(veiKategoriId='4566', riksveg=riksvegId, fylkesveg=fylkesvegId, europaveg=europavegId) +
                        "&antall=" + str(default_numrows))
        veg_dict = get_vei_referanser(vei_referanse_ider, vei_referanser_file)

    farts_demper_ider = get_json(api_base_url + "vegobjekter/103?"
                                                 "inkluder=lokasjon"
                                  "&antall=" + str(default_numrows))

    veg_dict_copy = veg_dict.copy()

    match_vei_referanser(farts_demper_ider, veg_dict_copy)

    data_frame = pd.DataFrame.from_dict({'fartsdempere': veg_dict_copy})
    print(data_frame)
    print(data_frame.count())
