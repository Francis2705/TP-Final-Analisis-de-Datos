import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("datos_filtrados_amba.txt", sep=';')

# Conversión de tipos
df['P47T'] = pd.to_numeric(df['P47T'], errors='coerce')
df['PONDII'] = pd.to_numeric(df['PONDII'], errors='coerce')
df['CH04'] = pd.to_numeric(df['CH04'], errors='coerce')
df['CH06'] = pd.to_numeric(df['CH06'], errors='coerce')
df['NIVEL_ED'] = pd.to_numeric(df['NIVEL_ED'], errors='coerce')
df['PP04D_COD'] = pd.to_numeric(df['PP04D_COD'], errors='coerce')

# Filtrar datos válidos
df = df[
    (df['P47T'] > 0) &
    (df['PONDII'] > 0) &
    (df['CH04'].isin([1, 2])) &
    (df['CH06'] > 0) &
    (df['NIVEL_ED'].isin([1, 2, 3, 4, 5, 6])) &  # excluye Ns/Nr y sin instrucción
    (df['PP04D_COD'].notna()) &
    (df['PP04D_COD'] > 0)
]

# Extraer tipo de relación laboral (3er dígito)
df['TIPO_RELACION'] = df['PP04D_COD'].astype(int).astype(str).str.zfill(5).str[2]
df = df[df['TIPO_RELACION'].isin(['0', '1', '2', '3'])]

df['TIPO_RELACION'] = df['TIPO_RELACION'].map({
    '0': 'Dirección',
    '1': 'Cuenta propia',
    '2': 'Jefes',
    '3': 'Asalariados'
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

# Factores IPC 2024
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
df_grouped = df.groupby(['TIPO_RELACION', 'NIVEL_ED', 'CH04', 'CH06']).apply(
    lambda x: np.average(x['INGRESO_REAL'], weights=x['PONDII'])
).reset_index(name='Ingreso promedio (real)')

# print(df_grouped)

encoder = OneHotEncoder(sparse_output=False, drop=None) #para analizar variables categoricas (fueron transformadas a binarias y se utiliza
# el onehotencoder)
x_cat = df_grouped[['TIPO_RELACION', 'NIVEL_ED', 'CH04']]
x_enconded = encoder.fit_transform(x_cat)
x_enconded_df = pd.DataFrame(x_enconded, columns=encoder.get_feature_names_out())
df_enconded_final = pd.concat([df_grouped.drop(columns=['TIPO_RELACION', 'NIVEL_ED', 'CH04']), x_enconded_df], axis=1)
df_enconded_final['Ingreso promedio (real)'] = df_grouped['Ingreso promedio (real)']

print(df_enconded_final) #hasta aca esta todo bien
#armar mas lindo el grafico con nombre mas descriptivos

plt.figure(figsize=(8, 6))
sns.heatmap(df_enconded_final.corr(), annot=True, cmap="coolwarm")
plt.title("🟦 Relacion de variables")
plt.tight_layout()
plt.show()