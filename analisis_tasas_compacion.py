import matplotlib.pyplot as plt
from analisis_tasa_actividad import df_actividad
from analisis_tasa_empleo import df_empleo
from analisis_tasa_desocupacion import df_tasa_anual

# Unir los tres DataFrames en uno solo por año
df_tasas = df_actividad.merge(df_empleo, on='anio').merge(df_tasa_anual, on='anio')

# Gráfico comparativo
plt.figure(figsize=(12, 6))

plt.plot(df_tasas['anio'], df_tasas['tasa_actividad'], marker='o', label='Tasa de Actividad (%)', color='blue')
plt.plot(df_tasas['anio'], df_tasas['tasa_empleo'], marker='o', label='Tasa de Empleo (%)', color='green')
plt.plot(df_tasas['anio'], df_tasas['tasa_desocupacion'], marker='o', label='Tasa de Desocupación (%)', color='crimson')

plt.title("📊 Evolución de Indicadores Laborales en el AMBA (2016-2024)", fontsize=14)
plt.xlabel("Año")
plt.ylabel("Porcentaje (%)")
plt.xticks(df_tasas['anio'])
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()