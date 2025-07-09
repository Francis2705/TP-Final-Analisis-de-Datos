import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
import numpy as np

def realizar_grafico_con_variable():
    aglomerado = gpd.read_file('aglomerados_eph.json')
    codigos_buenos_aires = ["32", "33"]
    buenos_aires = aglomerado[aglomerado['eph_codagl'].astype(str).isin(codigos_buenos_aires)].copy()
    buenos_aires["eph_codagl"] = buenos_aires["eph_codagl"].astype(int)

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

    df = pd.read_csv("datos_filtrados_amba.txt", sep=';', low_memory=False)
    df["P47T"] = pd.to_numeric(df["P47T"], errors="coerce")
    df["PONDII"] = pd.to_numeric(df["PONDII"], errors="coerce")
    df["ANO4"] = pd.to_numeric(df["ANO4"], errors="coerce")
    df["factor_ipc"] = df["ANO4"].map(factores_ipc_2024)
    df["P47T_ajustado"] = df["P47T"] * df["factor_ipc"]
    df = df[(df["P47T"] > 0) & (df["factor_ipc"].notna()) & (df["PONDII"] > 0)]

    datos_eph = df.groupby("AGLOMERADO").apply(
        lambda x: np.average(x["P47T_ajustado"], weights=x["PONDII"])
    ).reset_index(name="ingreso_promedio_ajustado")

    # Merge de datos EPH con geometría de los aglomerados
    datos_enriquecidos = buenos_aires.merge(datos_eph, left_on="eph_codagl", right_on="AGLOMERADO")
    datos_enriquecidos = datos_enriquecidos.to_crs(epsg=3857)

    # Graficar mapa
    ax = datos_enriquecidos.plot(column='ingreso_promedio_ajustado', cmap='YlOrBr', legend=True, figsize=(8, 6), edgecolor='black', alpha=0.7)

    ctx.add_basemap(ax, crs=datos_enriquecidos.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    plt.title("Ingreso promedio ajustado a precios 2024 por aglomerado (EPH)", fontsize=14)
    plt.axis('off')
    plt.show()