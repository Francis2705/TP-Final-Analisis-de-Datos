import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors

import geopandas as gpd # para instalar geopandas:pip install geopandas

#sirve para recuperar mapas bases de internet
import contextily as ctx #pip install contextily

######################################## GRAFICO SIN VARIABLE ###########################################

def realizar_grafico_sin_variable():
    #carga el archivo como GeoDataFrame de GeoPandas
    #permite trabajar con los aglomerados geograficos como si fueran un DataFrame de Pandas
    aglomerado = gpd.read_file('aglomerados_eph.json') 

    #como BS AS esta dividida en multiple aglomerados
    #Filtramos el GeoDataFrame con los eph_codagl correspondientes a los aglomerados que estan en BS AS
    #eph_codagl: codigo numerico del aglomerado según la EPH. Por ejemplo, 32 para CABA y 33 para provincia

    codigos_buenos_aires = ["32", "33"]  # codigo eph

    #Buscamos en la columna eph_codagl y revisamos si el codigo coincide con alguno el de la lista
    #tendremos la parte de buenos aires para mostrar en el mapa
    buenos_aires = aglomerado[aglomerado['eph_codagl'].astype(str).isin(codigos_buenos_aires)]

    # lo convertimos a numero entero
    buenos_aires["eph_codagl"] = buenos_aires["eph_codagl"].astype(int)



    print(buenos_aires)

    """
        32: CABA
        33:PArtidos del GBA

    """

    #Es lo que permite ubicar los datos geográficos correctamente sobre un mapa.
    buenos_aires_filtrado = buenos_aires.to_crs(epsg=3857)

    # fifsize:tamaño del grafico
    #alpha:Transparencia
    #edgecolor='red':borde negro para los poligonos(marca los limites de los barrios,caba etc)
    ax = buenos_aires_filtrado.plot(column='eph_codagl', cmap='Set3',legend=True,figsize=(10, 10), alpha=0.5, edgecolor='red')

    #Esto permite ver los aglomerados superpuestos al mapa real.
    ctx.add_basemap(ax, crs=buenos_aires_filtrado.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    plt.title("Analizando aglomerados de todo Buenos Aires.")
    plt.axis('off')
    plt.show()




