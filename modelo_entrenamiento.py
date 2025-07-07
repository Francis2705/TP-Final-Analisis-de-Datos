import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# --- Cargar datos ---
df = pd.read_csv("datos_filtrados_amba.txt", sep=';', low_memory=False)

# --- Convertir columnas relevantes ---
columnas = ['P47T', 'NIVEL_ED', 'CH04', 'CH06', 'ANO4', 'PP03D', 'PP3E_TOT', 'PP3F_TOT', 'PP04A', 'P21']
for col in columnas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Factores IPC 2024 ---
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

# Ajustar P21 también a precios 2024
df['P21_REAL'] = df['P21'] * df['FACTOR_IPC']

# Ingreso real ajustado
df['INGRESO_REAL'] = df['P47T'] * df['FACTOR_IPC']

# --- Filtrar datos válidos ---
df_validos = df[
    (df['P47T'] > 0) &
    (df['INGRESO_REAL'] >= 200000) & (df['INGRESO_REAL'] <= 2000000) &
    (df['FACTOR_IPC'].notna()) &
    (df['NIVEL_ED'].isin(range(1, 7))) &
    (df['CH04'].isin([1, 2])) &
    (df['CH06'] > 0) &
    (df['PP04A'].isin([1, 2])) &  # estatal o privada
    (df['P21_REAL'] > 0)
]

# --- Filtrar datos faltantes ---
df_faltantes = df[
    (df['P47T'] == -9) &
    (df['FACTOR_IPC'].notna()) &
    (df['NIVEL_ED'].isin(range(1, 7))) &
    (df['CH04'].isin([1, 2])) &
    (df['CH06'] > 0) &
    (df['PP04A'].isin([1, 2])) &
    (df['P21_REAL'] > 0)
]

# --- Variables independientes y objetivo ---
X = df_validos[['NIVEL_ED', 'CH04', 'CH06', 'PP03D', 'PP3E_TOT', 'PP3F_TOT', 'PP04A', 'P21_REAL']]
y = np.log(df_validos['INGRESO_REAL'])  # logaritmo del ingreso real

# --- Preprocesamiento ---
categoricas = ['NIVEL_ED', 'CH04', 'PP04A']  # agregar PP04A a variables categóricas
preprocesamiento = ColumnTransformer([
    ('onehot', OneHotEncoder(drop='first'), categoricas)
], remainder='passthrough')

# --- Pipeline con Random Forest ---
modelo = Pipeline(steps=[
    ('pre', preprocesamiento),
    ('regresor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
])

# --- Train/Test split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- Entrenar modelo ---
modelo.fit(X_train, y_train)

# --- Evaluación ---
y_pred_log = modelo.predict(X_test)
y_pred = np.exp(y_pred_log)
y_test_exp = np.exp(y_test)

r2 = r2_score(y_test_exp, y_pred)
rmse = np.sqrt(mean_squared_error(y_test_exp, y_pred))
mae = mean_absolute_error(y_test_exp, y_pred)

print(f"🌲 R²: {r2:.4f}")
print(f"🌲 RMSE: ${rmse:,.2f}")
print(f"🌲 MAE: ${mae:,.2f}")

# --- Comparación visual (opcional) ---
comparacion = pd.DataFrame({
    'Ingreso_real_2024': y_test_exp,
    'Ingreso_predicho': y_pred
})
print("\n📋 Comparación de ingresos reales vs predichos:")
print(comparacion.round(2).head(15))