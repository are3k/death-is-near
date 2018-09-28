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
    headers = {'X-Client': 'SSB Hackaton', 'X-Kontaktperson': 'egk@ssb.no'}
    print(url)
    return get(url, headers=headers).json()


def get_vei_referanser(data, vei_referanser_file):
    vei_dict = dict()

    with open(vei_referanser_file, 'w') as f:
        while True:
            for vegref in data['objekter']:
                kortform = vegref['lokasjon']['vegreferanser'][0]['kortform']
                kortform_uten_meter_suffix = VEI_REF_MAL.match(kortform).group(1)
                if kortform_uten_meter_suffix not in vei_dict:
                    print(kortform_uten_meter_suffix)
                    vei_dict[kortform_uten_meter_suffix] = 0
                    f.write(kortform_uten_meter_suffix + "\n")
            if data['metadata']['returnert'] == default_numrows:
                print('ny side' + " etter " + str(data['metadata']['returnert']) + " treff")
                data = get_json(data['metadata']['neste']['href'])
            else:
                print("det var " + str(data['metadata']['returnert']) + " treff på siste side")
                print(len(data['objekter']))
                break

    return vei_dict


def get_egenskap(egenskaper, kode):
    for e in egenskaper:
        if str(e['id']) == kode:
            return e['verdi']


def kalkuler_verdi(jsonObjekt, vei_ref_teller, vei_ref_til_objektet_uten_meter_suffix):
    if str(jsonObjekt['metadata']['type']['id']) == trafikk_ulykke_id:
        antall_drepte = get_egenskap(jsonObjekt['egenskaper'], '5070')
        antall_meget_alvorlig_skadet = get_egenskap(jsonObjekt['egenskaper'], '5071')
        antall_alvorlig_skadet = get_egenskap(jsonObjekt['egenskaper'], '5072')
        antall_lettere_skadet = get_egenskap(jsonObjekt['egenskaper'], '5073')
        if antall_lettere_skadet is None:
            antall_lettere_skadet = 1
        if antall_alvorlig_skadet is None:
            antall_alvorlig_skadet = 1
        if antall_meget_alvorlig_skadet is None:
            antall_meget_alvorlig_skadet = 1
        if antall_drepte is None:
            antall_drepte = 1
        return antall_drepte * 10 + antall_meget_alvorlig_skadet * 8 + \
               antall_alvorlig_skadet * 6 + antall_lettere_skadet * 1
    elif str(jsonObjekt['metadata']['type']['id']) == vegskulder_id:
        if 'egenskaper' not in jsonObjekt:
            return 2
        type = get_egenskap(jsonObjekt['egenskaper'], '1224')
        vekt = 0
        if type is None:
            vekt = 2
        elif type == 'Skulder, grus':
            vekt = 1
        elif type == 'Skulder, asfalt':
            vekt = 3
        return vekt
    elif str(jsonObjekt['metadata']['type']['id']) == farts_demper_id \
        or str(jsonObjekt['metadata']['type']['id']) == svingerestriksjon_id \
        or str(jsonObjekt['metadata']['type']['id']) == vilt_fare_id \
        or str(jsonObjekt['metadata']['type']['id']) == fotoboks_id:
       return 1
    elif str(jsonObjekt['metadata']['type']['id']) == trafikk_mengde_id:
        trafikk_mengde = get_egenskap(jsonObjekt['egenskaper'], '4623')
        vei_ref_teller[vei_ref_til_objektet_uten_meter_suffix] += 1
        return trafikk_mengde
    elif str(jsonObjekt['metadata']['type']['id']) == vegbredde_id:
        vei_bredde = get_egenskap(jsonObjekt['egenskaper'], '5555')
        vei_ref_teller[vei_ref_til_objektet_uten_meter_suffix] += 1
        return vei_bredde
    elif str(jsonObjekt['metadata']['type']['id']) == fartsgrenser_id:
        fartsgrense = get_egenskap(jsonObjekt['egenskaper'], '2021')
        if fartsgrense != 0:
            vei_ref_teller[vei_ref_til_objektet_uten_meter_suffix] += 1
        return fartsgrense
    else:
        return 0

def match_vei_referanser(variabel_navn_i_data_frame, data, vei_ref_dict):
    vei_ref_teller = vei_ref_dict.copy()
    for x in vei_ref_teller:
        vei_ref_teller[x] = 1

    while True:
        for o in data['objekter']:
            if 'vegreferanser' in o['lokasjon']:
                # ta bare de objektene på ikke-kommunale veier
                if o['lokasjon']['vegreferanser'][0]['kommune'] == 0:
                    vei_ref_til_objektet = o['lokasjon']['vegreferanser'][0]['kortform']
                    vei_ref_til_objektet_uten_meter_suffix = VEI_REF_MAL.match(vei_ref_til_objektet).group(1)
                    if vei_ref_til_objektet_uten_meter_suffix in vei_ref_dict:
                        vei_ref_dict[vei_ref_til_objektet_uten_meter_suffix] += \
                            kalkuler_verdi(o, vei_ref_teller, vei_ref_til_objektet_uten_meter_suffix)
                    else:
                        print('veireferanse {} fra {} {} finnes ikke i veireferanse lista'
                              .format(vei_ref_til_objektet_uten_meter_suffix,
                                      variabel_navn_i_data_frame,
                                      o['id']))
            else:
                print(variabel_navn_i_data_frame + ' id {} har ikke veireferanse'.format(o['id']))
        if data['metadata']['returnert'] == default_numrows:
            # print('ny side' + " etter " + str(data['metadata']['returnert']) + " treff")
            data = get_json(data['metadata']['neste']['href'])
        else:
            print("det var " + str(data['metadata']['returnert']) + " treff på siste side")
            print(len(data['objekter']))
            break

    for x in vei_ref_dict:
        vei_ref_dict[x] = vei_ref_dict[x] / vei_ref_teller[x]

def les_vei_referanser_fra_fil(vei_dict):
    with open('vei_referanser.txt', 'r') as f:
        for line in f:
            line_without_newline = line.replace("\n", "")
            vei_dict[line_without_newline] = 0


def initialisere_vei_referanser(vei_referanser_file):
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
                                      .format(veiKategoriId='4566', riksveg=riksveg_id, fylkesveg=fylkesveg_id,
                                              europaveg=europaveg_id) +
                                      "&antall=" + str(default_numrows))
        veg_dict = get_vei_referanser(vei_referanse_ider, vei_referanser_file)

    return veg_dict


def get_data_frame(variabel_navn_i_data_frame, veg_dict, vei_objekt_id, legg_til_dato):
    url = '{}vegobjekter/{}?inkluder=lokasjon,egenskaper,metadata&antall={}'\
        .format(api_base_url, vei_objekt_id, str(default_numrows))

    if legg_til_dato:
        url += "&egenskap=({dato}>'{aar}')".format(dato=dato_id, aar=aar_2013)

    variabel_ider = get_json(url)
    match_vei_referanser(variabel_navn_i_data_frame, variabel_ider, veg_dict)
    return pd.DataFrame.from_dict({variabel_navn_i_data_frame: veg_dict})


if __name__ == '__main__':
    dato_id = '5055'
    aar_2013 = '2010-01-01'

    europaveg_id = '5492'
    riksveg_id = '5493'
    fylkesveg_id = '5494'

    farts_demper_id = '103'
    trafikk_mengde_id = '540'
    veg_standard_id = '541'
    fotoboks_id = '775'
    vegskulder_id = '269'
    vegdekke_klasse_id = '831'
    vegbredde_id = '583'
    svingerestriksjon_id = '573'
    vilt_fare_id = '291'
    fartsgrenser_id = '105'
    trafikk_ulykke_id = '570'

    vei_referanser_file = Path("vei_referanser.txt")
    veg_dict = initialisere_vei_referanser(vei_referanser_file)

    data_frame_farts_demper = get_data_frame('fartsdempere', veg_dict.copy(), farts_demper_id, False)
    data_frame_trafikk_mengde = get_data_frame('trafikk_mengde', veg_dict.copy(), trafikk_mengde_id, False)
    # data_frame_veg_standard = get_data_frame('veg_standard', veg_dict.copy(), veg_standard_id, False)
    data_frame_fotobokser = get_data_frame('fotobokser', veg_dict.copy(), fotoboks_id, False)
    data_frame_vegskulder = get_data_frame('vegskulder', veg_dict.copy(), vegskulder_id, False)
    # data_frame_vegdekke_klasse = get_data_frame('vegdekke_klasse', veg_dict.copy(), vegdekke_klasse_id, False)
    # data_frame_vegbredde = get_data_frame('vegbredde', veg_dict.copy(), vegbredde_id, False)
    data_frame_svingerestriksjon = get_data_frame('svingerestriksjon', veg_dict.copy(), svingerestriksjon_id, False)
    data_frame_vilt_fare = get_data_frame('vilt_fare', veg_dict.copy(), vilt_fare_id, False)
    data_frame_fartsgrense = get_data_frame('fartsgrense', veg_dict.copy(), fartsgrenser_id, False)
    data_frame_trafikk_ulykke = get_data_frame('trafikk_ulykke', veg_dict.copy(), trafikk_ulykke_id, False)

    resultat = data_frame_farts_demper
    resultat = resultat.join(data_frame_trafikk_mengde)
    # resultat = resultat.join(data_frame_veg_standard)
    resultat = resultat.join(data_frame_fotobokser)
    resultat = resultat.join(data_frame_vegskulder)
    # resultat = resultat.join(data_frame_vegdekke_klasse)
    # resultat = resultat.join(data_frame_vegbredde)
    resultat = resultat.join(data_frame_svingerestriksjon)
    resultat = resultat.join(data_frame_vilt_fare)
    resultat = resultat.join(data_frame_fartsgrense)
    resultat = resultat.join(data_frame_trafikk_ulykke)

    print(resultat)
    print(resultat.count())

    resultat.to_csv("datasett.csv")