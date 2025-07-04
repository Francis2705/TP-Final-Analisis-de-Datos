import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("datos_filtrados_amba.txt", sep=';')

# Filtrar ingresos válidos
df = df[(df['CH06'] > 15) & (df['P47T'] > 0) & (df['PONDII'] > 0)]

# Factores de ajuste a precios de 2024
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

# Cálculo de ingresos promedio por año
resultados = []

for anio, grupo in df.groupby('ANO4'):
    ingreso_total_ponderado = (grupo['P47T'] * grupo['PONDII']).sum()
    total_ponderacion = grupo['PONDII'].sum()

    if total_ponderacion > 0:
        ingreso_promedio_nominal = ingreso_total_ponderado / total_ponderacion
        ingreso_promedio_real = ingreso_promedio_nominal * factores_ipc_2024.get(anio, 1.0)
    else:
        ingreso_promedio_nominal = None
        ingreso_promedio_real = None

    resultados.append({
        'anio': anio,
        'ingreso_promedio_nominal': round(ingreso_promedio_nominal, 2),
        'ingreso_promedio_real': round(ingreso_promedio_real, 2)
    })

df_ingresos = pd.DataFrame(resultados).sort_values('anio')

# Mostrar la tabla
print(df_ingresos)

# Gráfico
plt.figure(figsize=(10, 6))
plt.plot(df_ingresos['anio'], df_ingresos['ingreso_promedio_nominal'], marker='o', label='Ingreso Nominal', color='orange')
plt.plot(df_ingresos['anio'], df_ingresos['ingreso_promedio_real'], marker='o', label='Ingreso Real (2024)', color='purple')
plt.title("💵 Evolución del Ingreso Promedio Individual en el AMBA (2016-2024)", fontsize=14)
plt.xlabel("Año")
plt.ylabel("Ingreso mensual (pesos de 2024)")
plt.xticks(df_ingresos['anio'])
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#fuentes consultadas:
    #https://estudiodelamo.com/inflacion-argentina-anual-mensual/
    #https://chequeado.com/inflacionacumulada/