import pandas as pd
import matplotlib.pyplot as plt

def mostrar_tasa_actividad(devolver_df=False):
    df = pd.read_csv('datos_filtrados_amba.txt', sep=';', header=0, low_memory=False)
    df_filtrado = df[(df['CH06'] > 9)] #se filtran mayores de 9 anios porque asi lo indica el INDEC
    resultados = []

    for anio, grupo in df_filtrado.groupby('ANO4'):
        ocupados = grupo[grupo['ESTADO'] == 1]['PONDERA'].sum()
        desocupados = grupo[grupo['ESTADO'] == 2]['PONDERA'].sum()
        pea = ocupados + desocupados
        poblacion_total = grupo['PONDERA'].sum()

        if poblacion_total > 0:
            tasa_actividad = (pea / poblacion_total) * 100
        else:
            tasa_actividad = None

        resultados.append({'anio': anio, 'tasa_actividad': round(tasa_actividad, 2)})

    df_actividad = pd.DataFrame(resultados).sort_values('anio')

    if(devolver_df):
        return df_actividad

    plt.figure(figsize=(10, 5))
    plt.plot(df_actividad['anio'], df_actividad['tasa_actividad'], marker='o', color='blue')
    plt.title("📈 Evolución Anual de la Tasa de Actividad en el AMBA (2016-2024)", fontsize=14)
    plt.xlabel("Año")
    plt.ylabel("Tasa de Actividad (%)")
    plt.xticks(df_actividad['anio'])
    plt.grid(True)
    plt.tight_layout()
    plt.show()