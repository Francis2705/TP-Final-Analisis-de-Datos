import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

def realizar_analisis_multivariado():
    df = pd.read_csv("datos_filtrados_amba.txt", sep=';', low_memory=False)
    df['P47T'] = pd.to_numeric(df['P47T'], errors='coerce')
    df['PONDII'] = pd.to_numeric(df['PONDII'], errors='coerce')
    df['CH04'] = pd.to_numeric(df['CH04'], errors='coerce')
    df['CH06'] = pd.to_numeric(df['CH06'], errors='coerce')
    df['NIVEL_ED'] = pd.to_numeric(df['NIVEL_ED'], errors='coerce')
    df['PP04D_COD'] = pd.to_numeric(df['PP04D_COD'], errors='coerce')

    df = df[
        (df['P47T'] > 0) &
        (df['PONDII'] > 0) &
        (df['CH04'].isin([1, 2])) &
        (df['CH06'] > 0) &
        (df['NIVEL_ED'].isin([1, 2, 3, 4, 5, 6])) &
        (df['PP04D_COD'].notna()) &
        (df['PP04D_COD'] > 0)
    ]

    # Extraer calificacion ocupacional
    df['CALIFICACION_OCUPACIONAL'] = df['PP04D_COD'].astype(int).astype(str).str.zfill(5).str[-1]
    df = df[df['CALIFICACION_OCUPACIONAL'].isin(['1', '2', '3', '4'])]

    df['CALIFICACION_OCUPACIONAL'] = df['CALIFICACION_OCUPACIONAL'].map({
        '1': 'Profesionales',
        '2': 'Tecnicos',
        '3': 'Operativo',
        '4': 'No calificado'
    })

    # Mapas de etiquetas
    df['CH04'] = df['CH04'].map({1: 'Varón', 2: 'Mujer'})
    df['NIVEL_ED'] = df['NIVEL_ED'].map({
        1: 'Prim. Incomp.',
        2: 'Prim. Comp.',
        3: 'Sec. Incomp.',
        4: 'Sec. Comp.',
        5: 'Univ. Incomp.',
        6: 'Univ. Comp.'
    })

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
    df['FACTOR_IPC'] = df['ANO4'].map(factores_ipc_2024)
    df['INGRESO_REAL'] = df['P47T'] * df['FACTOR_IPC']

    # Agrupar y calcular ingreso promedio ponderado
    df_grouped = df.groupby(['CALIFICACION_OCUPACIONAL', 'NIVEL_ED', 'CH04', 'CH06']).apply(
        lambda x: np.average(x['INGRESO_REAL'], weights=x['PONDII'])
    ).reset_index(name='Ingreso promedio (real)')

    # Para analizar variables categoricas (fueron transformadas a binarias y se utiliza el OneHotEncoder)
    encoder = OneHotEncoder(sparse_output=False, drop=None)
    x_cat = df_grouped[['CALIFICACION_OCUPACIONAL', 'NIVEL_ED', 'CH04']]
    x_enconded = encoder.fit_transform(x_cat)
    x_enconded_df = pd.DataFrame(x_enconded, columns=encoder.get_feature_names_out())
    df_enconded_final = pd.concat([df_grouped.drop(columns=['CALIFICACION_OCUPACIONAL', 'NIVEL_ED', 'CH04']), x_enconded_df], axis=1)
    df_enconded_final['Ingreso promedio (real)'] = df_grouped['Ingreso promedio (real)']

    # Renombrar columnas con nombres más legibles
    df_enconded_final.rename(columns={
        'CH06': 'Edad',
        'CALIFICACION_OCUPACIONAL_No calificado': 'No calificado',
        'CALIFICACION_OCUPACIONAL_Operativo': 'Operativo',
        'CALIFICACION_OCUPACIONAL_Profesionales': 'Profesionales',
        'CALIFICACION_OCUPACIONAL_Tecnicos': 'Tecnicos',
        'NIVEL_ED_Prim. Comp.': 'Primario completo',
        'NIVEL_ED_Prim. Incomp.': 'Primario incompleto',
        'NIVEL_ED_Sec. Comp.': 'Secundario completo',
        'NIVEL_ED_Sec. Incomp.': 'Secundario incompleto',
        'NIVEL_ED_Univ. Comp.': 'Universitario completo',
        'NIVEL_ED_Univ. Incomp.': 'Universitario incompleto',
        'CH04_Mujer': 'Mujer',
        'CH04_Varón': 'Hombre'
    }, inplace=True)

    plt.figure(figsize=(12, 6))
    sns.heatmap(df_enconded_final.corr(), annot=True, cmap="coolwarm")
    plt.title("Relacion de variables")
    plt.tight_layout()
    plt.show()