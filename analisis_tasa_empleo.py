import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('datos_filtrados_amba.txt', sep=';', header=0, low_memory=False)
df_filtrado = df[(df['CH06'] > 15) & (df['ESTADO'].isin([1, 2]))] #filtrar mayores a 15 anios (16 es la edad legal laboral) y con ESTADO válido
resultados = []

for anio, grupo in df.groupby('ANO4'):
    ocupados = grupo[grupo['ESTADO'] == 1]['PONDERA'].sum()
    poblacion_total = grupo['PONDERA'].sum()

    if poblacion_total > 0:
        tasa_empleo = (ocupados / poblacion_total) * 100 #calculo de la tasa de empleo
    else:
        tasa_empleo = None

    resultados.append({'anio': anio, 'tasa_empleo': round(tasa_empleo, 2)})

# Crear DataFrame de resultados
df_empleo = pd.DataFrame(resultados).sort_values('anio')

# Graficar
plt.figure(figsize=(10, 5))
plt.plot(df_empleo['anio'], df_empleo['tasa_empleo'], marker='o', color='green')
plt.title("📈 Evolución Anual de la Tasa de Empleo en el AMBA (2016-2024)", fontsize=14)
plt.xlabel("Año")
plt.ylabel("Tasa de Empleo (%)")
plt.xticks(df_empleo['anio'])
plt.grid(True)
plt.tight_layout()
plt.show()