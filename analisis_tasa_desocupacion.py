import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('datos_filtrados_amba.txt', sep=';', header=0, low_memory=False)
df_filtrado = df[(df['CH06'] > 15) & (df['ESTADO'].isin([1, 2]))] #filtrar mayores a 15 anios (16 es la edad legal laboral) y con ESTADO válido
resultados = []

for anio, grupo in df_filtrado.groupby('ANO4'):
    ocupados = grupo[grupo['ESTADO'] == 1]['PONDERA'].sum()
    desocupados = grupo[grupo['ESTADO'] == 2]['PONDERA'].sum()
    pea = ocupados + desocupados

    if pea > 0:
        tasa = (desocupados / pea) * 100 #calculo de la tasa de desocupacion
    else:
        tasa = None

    resultados.append({'anio': anio, 'tasa_desocupacion': round(tasa, 2)})
    # print(resultados[-1])
    # en el 2016, la tasa promedio de desocupacion en el amba fue de 9.69

# Crear DataFrame de resultados
df_tasa_anual = pd.DataFrame(resultados).sort_values('anio')

# Graficar
plt.figure(figsize=(10, 5))
plt.plot(df_tasa_anual['anio'], df_tasa_anual['tasa_desocupacion'], marker='o', color='darkred')
plt.title("📈 Evolución Anual de la Tasa de Desocupación en el AMBA (2016-2024)", fontsize=14)
plt.xlabel("Año")
plt.ylabel("Tasa de Desocupación (%)")
plt.xticks(df_tasa_anual['anio'])
plt.grid(True)
plt.tight_layout()
plt.show()

#el grafico muestra:
    #en el eje x los anios
    #en el eje y la tasa de desocupacion
    #y cada punto representa la tasa promedio anual de ese anio (promedio ponderado de los 4 trimestres)
    #NO SIGNIFICA QUE EN EL ULTIMO TRIMESTRE DEL ANIO LA TASA DE DESOCUPACION FUE ESA, sino que el promedio de los 4 trimestres dio ese num