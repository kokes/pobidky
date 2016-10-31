"""
Mirne ocisti seznam prijemcu pobidek, doplni ICO na zaklade slovniku
a ulozi do CSV
"""

import pandas as pd
import numpy as np

df = pd.read_excel('cache/data.xls', sheetname='PROJEKTY', skiprows=1)


# odsekej paticku
df = df.loc[df['Pořadové číslo'].apply(lambda x: str(x).isdigit())]

cls = 'cislo, spol, ico, sektor, nace, druh, zeme, inv_eur, inv_usd, inv_czk, nova_mista, pod_dane, pob_mista, pob_rekv, pob_pozem, \
pob_kap, mira_podpory, strop, okres, kraj, region_nuts, podani, rozh_den, rozh_mesic, rozh_rok, msp, zruseno'.split(', ')

df.columns = cls

df.spol = df.spol.apply(str.strip)
df.loc[~df.ico.isnull(), 'ico'] = df.ico.loc[~df.ico.isnull()].apply(lambda x: int(str(x).replace(' ', '')))

len(df), df.ico.isnull().sum()

sl = pd.read_csv('slovnik.csv', dtype=str).set_index('czechinvest').to_dict()['ico']

chyb = df.loc[df.spol.apply(lambda x: x not in sl)]
assert len(chyb) == 0

# vypln chybejici ico
for rw in df.loc[df.ico.isnull()].iterrows():
    df.loc[rw[0], 'ico'] = int(sl[rw[1].spol])

# nahrad necisty nazvy pomoci unifikace ICO
# len(df.ico.unique()), len(df.spol.unique())
for g in df.groupby('ico'):
    if len(g[1]) == 1: continue # uz unifikovany
    df.loc[df.ico == g[0], 'spol'] = g[1]['spol'].iloc[0]

assert len(df.ico.unique()) == len(df.spol.unique())

# cisti cisla a tak

df.strop = df.strop.replace('-', np.nan).astype(float)
df.podani = df.podani.astype(int)
df.msp = (df.msp.replace('Ne', False).replace('Ano', True)).astype(bool)
df.zruseno = df.zruseno.replace('x', True).replace(np.nan, False).astype(bool)

df.to_csv('data.csv', index=None)