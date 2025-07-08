import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import geopandas as gpd # para instalar geopandas:pip install geopandas

#sirve para recuperar mapas bases de internet
import contextily as ctx #pip install contextily

def realizar_grafico_con_variable():
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

    """
        Mostramos los aglomerados de Buenos Aires,tanto de caba como de pba,usando
        el promedio de la variable P47T como referencia para el color

    """

    #definimos los factores IPC para ajustar a valores constantes 2024
    factores_ipc_2024 = {
        2016: 53.93,
        2017: 40.07,
        2018: 32.10,
        2019: 21.73,
        2020: 14.12,
        2021: 10.38,
        2022: 6.88,
        2023: 3.18,
        2024: 1.00,
    }

    df = pd.read_csv("datos_filtrados_amba.txt", sep=';')

    # Convertir columna a numérica si hay valores no válidos
    df["P47T"] = pd.to_numeric(df["P47T"], errors="coerce")

    #Creamos nueva columna con el factor según el año de cada fila
    df["factor_ipc"] = df["ANO4"].map(factores_ipc_2024)

    #Calculamos el ingreso ajustado por inflación
    df["P47T_ajustado"] = df["P47T"] * df["factor_ipc"]

    # agrupamos por aglomerado y calcular ingreso promedio ajustado
    datos_eph = df.groupby("AGLOMERADO", as_index=False)["P47T_ajustado"].mean()
    datos_eph.rename(columns={"P47T_ajustado": "ingreso_promedio_ajustado"}, inplace=True)

    # Hacer el merge:Operacion para juntar dos tablas,es decir,dos dataframes
    # left_on: columna del DataFrame izquierdo que se usará para emparejar
    # right_on: columna del DataFrame derecho para emparejar
    # Merge con buenos_aires
    datos_enriquecidos = buenos_aires.merge(datos_eph, left_on="eph_codagl", right_on="AGLOMERADO")
    datos_enriquecidos = datos_enriquecidos.to_crs(epsg=3857)

    # Mapa usando ingreso ajustado
    ax = datos_enriquecidos.plot(column='ingreso_promedio_ajustado',
                                    cmap='YlOrBr',
                                    legend=True,
                                    figsize=(10, 10),
                                    edgecolor='black',
                                    alpha=0.7)

    ctx.add_basemap(ax, crs=datos_enriquecidos.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    plt.title("Ingreso promedio ajustado a precios 2024 por aglomerado (EPH)")
    plt.axis('off')
    plt.show()