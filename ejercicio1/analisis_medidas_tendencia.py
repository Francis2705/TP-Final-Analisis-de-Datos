import pandas as pd
import matplotlib.pyplot as plt

def ver_evolucion_medidas_tendecia_central():
    df = pd.read_csv("datos_filtrados_amba.txt", sep=';', low_memory=False)
    df['P47T'] = pd.to_numeric(df['P47T'], errors='coerce')
    df['PONDII'] = pd.to_numeric(df['PONDII'], errors='coerce')
    df = df[(df['P47T'] > 0) & (df['PONDII'] > 0)]

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

    # Calcular media y mediana ponderadas por año
    resultados = []

    for anio, grupo in df.groupby('ANO4'):
        ipc_factor = factores_ipc_2024.get(anio, 1.0)

        # Media ponderada
        ingreso_total = (grupo['P47T'] * grupo['PONDII']).sum()
        total_ponderacion = grupo['PONDII'].sum()
        media_nominal = ingreso_total / total_ponderacion
        media_real = media_nominal * ipc_factor

        # Mediana ponderada
        grupo_ordenado = grupo.sort_values('P47T')
        grupo_ordenado['pond_acum'] = grupo_ordenado['PONDII'].cumsum()
        mitad_ponderacion = grupo_ordenado['PONDII'].sum() / 2
        mediana_nominal = grupo_ordenado.loc[grupo_ordenado['pond_acum'] >= mitad_ponderacion, 'P47T'].iloc[0]
        mediana_real = mediana_nominal * ipc_factor

        resultados.append({
            'anio': anio,
            'media_real': round(media_real, 2),
            'mediana_real': round(mediana_real, 2)
        })

    df_medidas = pd.DataFrame(resultados).sort_values('anio')

    # Gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_medidas['anio'], df_medidas['media_real'], marker='o', label='Media (real)', color='green')
    plt.plot(df_medidas['anio'], df_medidas['mediana_real'], marker='o', label='Mediana (real)', color='red')

    plt.title("📊 Evolución de la Media y Mediana de Ingresos Totales Individuales (P47T, precios de 2024)", fontsize=13)
    plt.xlabel("Año")
    plt.ylabel("Ingreso mensual (pesos de 2024)")
    plt.xticks(df_medidas['anio'])
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()