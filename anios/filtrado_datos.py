import pandas as pd
from glob import glob

archivos = sorted(glob("anios/usu_individual_T*.txt")) #busca todos los archivos que empiecen con "usu_individual_T" y terminen en ".txt"
dataframes = []

for archivo in archivos:
    print(f"📥 Cargando {archivo}")
    df = pd.read_csv(archivo, sep=';', header=0, low_memory=False)
    dataframes.append(df)

df_total = pd.concat(dataframes, ignore_index=True) #uno todos los dataframes en uno solo

print(f"\n✅ Cargados {len(archivos)} archivos. Total de filas: {len(df_total):,}")

df_total = df_total.drop_duplicates() #1. Eliminar duplicados
df_amba = df_total[(df_total['REGION'] == 1) & (df_total['AGLOMERADO'].isin([32, 33]))].copy() #2. Filtrar por AMBA

print(f"✅ Filtrado por AMBA completado. Filas resultantes: {len(df_amba):,}")

df_amba.to_csv("datos_filtrados_amba.txt", sep=";", index=False)
print("✅ Guardado como datos_filtrados_amba.txt")