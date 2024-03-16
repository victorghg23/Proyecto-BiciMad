import pandas as pd
import numpy as np
import requests as req
import json
import ast
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from geopy.distance import geodesic
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import argparse

csv_bicimad = pd.read_csv('/Users/victor/Documents/Laboratorios IronHack/Proyecto-BiciMad/datos/bicimad_stations.csv', sep = '\t')

'''
ELIMINAMOS LA COLUMNA QUE NO NOS INTERESA
'''

csv_bicimad = csv_bicimad.drop('Unnamed: 0', axis = 1)

'''
USANDO LOS DATOS Y TENIENDO EN CUENTA QUE LAS COORDENADAS SON UNA STING,
VAMOS A PASAR LAS COORDENADAS DE STRING A LISTA PARA PODER TRATAR CON ELLAS
EN LA SIGUIENTE CELDA DE CÓDIGO
'''

csv_bicimad['geometry.coordinates'] = csv_bicimad['geometry.coordinates'].apply(ast.literal_eval)

'''
UNA VEZ QUE TENEMOS LOS DATOS EN FORMATO LISTA, LE PIDO QUE ME PASE 
EL PRIMER ELEMENTO A OTRA COLUMNA LLAMADA 'LONGITUD', Y EL SEGUNDO
ELEMENTO A OTRA COLUMNA LLAMADA LATITUD
'''

csv_bicimad['Latitud'] = csv_bicimad['geometry.coordinates'].apply(lambda x: x[1])
csv_bicimad['Longitud'] = csv_bicimad['geometry.coordinates'].apply(lambda x: x[0])

'''
EXTRAEMOS LOS DATOS DEL PORTAL DE DATOS ABIERTOS DEL AYUNTAMIENTO DE MADRID
'''

url = 'https://datos.madrid.es/egob/catalogo/300356-0-monumentos-ciudad-madrid.json'

monumentos = req.get(url)

'''
EXTRAEMOS LOS DATOS DE LA KEY QUE NOS INTERESA
'''

datos_mon = monumentos.json()['@graph']

'''
CREAMOS EL DATAFRAME DE LOS MONUMENTOS
'''

df_mon = pd.json_normalize(datos_mon)

'''
ELIMINAMOS LAS COL QUE NO NOS INTERESAN
'''

df_mon = df_mon.drop(['@id', 'id', 'relation', 'references', 'address.district.@id', 'address.locality', 'address.postal-code', 'organization.organization-desc', 'organization.organization-name', 'address.area.@id'], axis=1)

'''
CAMBIAMOS LOS NOMBRES DE LAS COLUMNAS
'''

df_mon = df_mon.set_axis(['Monumento', 'Localización', 'Latitud', 'Longitud'], axis=1)

'''
ELIMINAMOS TODAS LAS FILAS QUE CONTENGAN NAN
'''

df_mon = df_mon.dropna().reset_index(drop=True)

'''
CREAMOS UN ARGPARSER
'''

parser = argparse.ArgumentParser(description='Programa para encontrar la estación de BiciMAD más cercana a un monumento en Madrid.')
parser.add_argument('-e', '--estacion', type = int, help='Número de la estación de BiciMAD donde te encuentras.')
parser.add_argument('-m', '--monumento', type = str, help='Nombre del monumento al que deseas ir.')

args = parser.parse_args()
origen = args.estacion
destino = args.monumento


'''
EN FUNCIÓN DEL NÚMERO DE ESTACIÓN QUE SE PONGA, ME DARA LA FILA QUE DESEO
'''

bicimad_input = csv_bicimad[csv_bicimad['id'] == origen][['name','address', 'Latitud', 'Longitud']]

df_mon['fuzzy' ]= df_mon['Monumento'].apply(lambda x: fuzz.partial_ratio(x, destino))

df_mon_fuzzy = df_mon[df_mon.fuzzy==df_mon.fuzzy.max()]

monumento_latitud = df_mon_fuzzy['Latitud'].iloc[0]
monumento_longitud = df_mon_fuzzy['Longitud'].iloc[0]

estaciones_candidatas = []

for index, estacion in csv_bicimad.iterrows():
    
    if estacion['light'] != 3 and estacion['activate'] == 1 and estacion['no_available'] == 0 and estacion['free_bases'] != 0:

        distancia = geodesic((monumento_latitud, monumento_longitud), (estacion['geometry.coordinates'][1], estacion['geometry.coordinates'][0])).kilometers

        distancia = round(distancia, 3)
        
        estaciones_candidatas.append({'Nombre': estacion['name'], 'Distancia': distancia})

        estaciones_candidatas = sorted(estaciones_candidatas, key=lambda x: x['Distancia'])


estacion_cercana = None
for estacion in estaciones_candidatas:
    if not estacion_cercana or (estacion_cercana['light'] == 3 and estacion_cercana['activate'] == 0
                                and estacion_cercana['no_available'] == 1 and estacion_cercana['free_bases'] == 0):
        estacion_cercana = estacion
        break
estaciones_candidatas[0]
df_bicimad_cercana = pd.DataFrame([estaciones_candidatas[0]])

'''
CONCATENO LOS DATA FRAME DE BICIMAD Y DE MONUMENTOS
'''

df_bicimad_mon = pd.concat([df_mon_fuzzy, df_bicimad_cercana], axis = 1)
df_bicimad_mon = df_bicimad_mon.drop(['fuzzy'], axis = 1)
df_bicimad_mon = df_bicimad_mon.set_axis(['Monumento', 'Ubicación del Monumento', 'Latitud', 'Longitud', 'Estación más Cercana', 'Distancia al Monumento'], axis=1)
df_bicimad_mon = df_bicimad_mon.drop(['Latitud', 'Longitud'], axis = 1)

'''
ELIMINAMOS LOS NAN
'''

df_finish = df_bicimad_mon.fillna('')

'''
CREAMOS UN DATAFRAME DE UNA SOLA LINEA EN LUGAR DE DOS, QUE ES COMO APARECE 
EN LA ANTERIOR LINEA DE CÓDIGO
'''

list_1 = df_finish['Monumento'].to_list()
list_2 = df_finish['Ubicación del Monumento'].to_list()
list_3 = df_finish['Estación más Cercana'].to_list()
list_4 = df_finish['Distancia al Monumento'].to_list()

df_finish = pd.DataFrame({'Monumento': [list_1[0]], 
            'Ubicación del Monumento': [list_2[0]],
             'Estación más Cercana': [list_3[1]],
             'Distancia al Monumento': [list_4[1]]
            })
print(df_finish)

'''
AQUÍ NOS DIRÁ EN UNA FRASE CUÁL ES LA ESTACIÓN MÁS CERCANA Y LA DISTANCIA A 
LA QUE SE ENCUENTRA DEL MONUMENTO EN METROS
'''

print(f"La estación más cercana al monumento es '{estacion_cercana['Nombre']}', ubicada a {estacion_cercana['Distancia'] * 1000:.1f} metros.")