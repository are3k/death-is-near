#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 09:27:36 2018

@author: karihelena
"""

import pandas as pd
import numpy as np


def lagStrekning(df):
    fylke = df['fylkesnummer'].astype(str)
    kom = df['kommunenummer'].astype(str)
    vegk = df['vegkategori']
    vegs = df['vegstatus']
    vegnr = df['vegnummer'].astype(str)
    hp = df['fra hp'].astype(str)
    strekning = fylke + kom + vegk + vegs + vegnr +"hp"+ hp
    return strekning

def lagTeller(df, navn, verdier):
    data = pd.DataFrame({'strekning': lagStrekning(df),
                   navn: verdier})
    teller = data.groupby('strekning')[navn].sum().reset_index()
    teller = teller.set_index('strekning')
    return teller

# Tar ut eksisterende veier:
data_532 = pd.read_csv('532-vegref.csv',sep=';')
veier = data_532['Vegstatus']=="Eksisterende veg"

# Lager X matrise med kun strekninger + strekninger som index
strekning = pd.unique(lagStrekning(data_532.loc[veier]))
X = pd.DataFrame({'strekning':strekning})
X.index = strekninger['strekning']

# Legge til variabler:

fartsdemper     = pd.read_csv('103-fartsdemper.csv', sep=';')
fartsdemper = lagTeller(fartsdemper, 'fartsdemper', \
                        np.ones(np.shape(fartsdemper)[0]) )
X = X.join(fartsdemper).fillna(0)

vegskulder      = pd.read_csv('269-vegskulder.csv',sep=';')
typer = (vegskulder['Type']=="Skulder, asfalt")*3+\
            (pd.isnull(vegskulder['Type']))*2+\
            (vegskulder['Type']=="Skulder, grus")*1
vegskulder = lagTeller(vegskulder, 'vegskulder', typer)
X = X.join(vegskulder).fillna(0)



'''
viltfare        = pd.read_csv('291-viltfare.csv',
                        sep=';', index_col='vegreferanse')
vegbredde       = pd.read_csv('583-vegbredde.csv',
                        sep=';', index_col='vegreferanse')
trafikkmengde   = pd.read_csv('540-trafikkmengde.csv',
                        sep=';', index_col='vegreferanse')
vegstandard     = pd.read_csv('541-vegstandard.csv',
                        sep=';', index_col='vegreferanse')
ulykker         = pd.read_csv('570-trafikkulykke.csv',
                        sep=';', index_col='vegreferanse')
svingerestriksjon = pd.read_csv('573-svingerestriksjon.csv',
                        sep=';', index_col='vegreferanse')
veitiltak       = pd.read_csv('575-veitiltak.csv',
                        sep=';', index_col='vegreferanse')
kontroller      = pd.read_csv('775-atk.csv',
                        sep=';', index_col='vegreferanse')
vegdekkeklasse  = pd.read_csv('831-vegdekkeklasse.csv',
                        sep=';', index_col='vegreferanse')

vegbredde = pd.DataFrame(vegbredde.Dekkebredde)
vegstatus = pd.DataFrame(data_831.vegstatus)
viltfare = pd.DataFrame(vegskulder.)
ulykker = pd.DataFrame(ulykker.)

###### testing ##### 


vegref0 = vegref.loc[1:10,]

matrise = vegref.join(vegbredde)
vegskulder.Type.value_counts(dropna=False)
''''