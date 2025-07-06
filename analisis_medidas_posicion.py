import pandas as pd
import matplotlib.pyplot as plt

#hacer archivo aparte para la p21

# Cargar el archivo filtrado
df = pd.read_csv("datos_filtrados_amba.txt", sep=';', low_memory=False)

# Convertir columnas necesarias
df['P47T'] = pd.to_numeric(df['P47T'], errors='coerce')
df['PONDII'] = pd.to_numeric(df['PONDII'], errors='coerce')

# Filtrar casos válidos
df = df[(df['P47T'] > 0) & (df['PONDII'] > 0)]

# Factores IPC a precios 2024
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

# Función para obtener percentil ponderado
def percentil_ponderado(grupo, variable, ponderador, percentil):
    df_ordenado = grupo.sort_values(variable).copy()
    df_ordenado['pond_acum'] = df_ordenado[ponderador].cumsum()
    total_pond = df_ordenado[ponderador].sum()
    umbral = total_pond * percentil
    valor = df_ordenado[df_ordenado['pond_acum'] >= umbral][variable].iloc[0]
    return valor

# Calcular medidas de posición por año
resultados = []

for anio, grupo in df.groupby('ANO4'):
    ipc_factor = factores_ipc_2024.get(anio, 1.0)
    
    p10 = percentil_ponderado(grupo, 'P47T', 'PONDII', 0.10) * ipc_factor
    p25 = percentil_ponderado(grupo, 'P47T', 'PONDII', 0.25) * ipc_factor
    p50 = percentil_ponderado(grupo, 'P47T', 'PONDII', 0.50) * ipc_factor
    p75 = percentil_ponderado(grupo, 'P47T', 'PONDII', 0.75) * ipc_factor
    p90 = percentil_ponderado(grupo, 'P47T', 'PONDII', 0.90) * ipc_factor

    resultados.append({
        'anio': anio,
        'P10': round(p10, 2),
        'P25': round(p25, 2),
        'P50 (mediana)': round(p50, 2),
        'P75': round(p75, 2),
        'P90': round(p90, 2),
    })

df_posicion = pd.DataFrame(resultados).sort_values('anio')
print(df_posicion)

# Gráfico de evolución de percentiles
plt.figure(figsize=(12, 6))
plt.plot(df_posicion['anio'], df_posicion['P10'], marker='o', label='P10 (percentil 10)', color='gray')
plt.plot(df_posicion['anio'], df_posicion['P25'], marker='o', label='P25 (Q1)', color='blue')
plt.plot(df_posicion['anio'], df_posicion['P50 (mediana)'], marker='o', label='P50 (mediana)', color='green')
plt.plot(df_posicion['anio'], df_posicion['P75'], marker='o', label='P75 (Q3)', color='orange')
plt.plot(df_posicion['anio'], df_posicion['P90'], marker='o', label='P90', color='red')

plt.title("📈 Evolución de Percentiles de Ingreso Individual (P47T, precios 2024)", fontsize=14)
plt.xlabel("Año")
plt.ylabel("Ingreso mensual (pesos de 2024)")
plt.xticks(df_posicion['anio'])
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
