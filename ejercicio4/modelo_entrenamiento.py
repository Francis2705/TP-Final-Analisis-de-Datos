import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def realizar_prediccion():
    df = pd.read_csv("datos_filtrados_amba.txt", sep=';', low_memory=False)

    columnas = ['P47T', 'NIVEL_ED', 'CH04', 'CH06', 'ANO4', 'PP03D', 'PP3E_TOT', 'PP3F_TOT', 'PP04A',
                'P21', 'PP07H', 'PP07G1', 'PP07G2', 'PP07G3', 'PP07G4', 'ESTADO']
    for col in columnas:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    factores_ipc_2024 = {2016: 53.93, 2017: 40.07, 2018: 32.10, 2019: 21.73, 2020: 14.12, 2021: 10.38, 2022: 6.88, 2023: 3.18, 2024: 1.00}
    df['FACTOR_IPC'] = df['ANO4'].map(factores_ipc_2024)

    df['P21_REAL'] = df['P21'] * df['FACTOR_IPC']
    df['P47T_REAL'] = df['P47T'] * df['FACTOR_IPC']

    #Filtrar datos validos y outliers
    df_validos = df[
        (df['P47T_REAL'] >= 100000) & (df['P47T_REAL'] <= 6000000) & #ingresos totales entre 100.000 y 6.000.000
        (df['P21_REAL'] > 120000) & #ingreso de la ocupacion principal (se filtra por mayor a 100 dolares aproximadamente)
        (df['CH06'] > 5) & #edad mayor a 5 anios (edad minima que se considera para empezar a tener algun ingreso como un regalo, premio, etc)
        (df['FACTOR_IPC'].notna()) & #que el factor IPC no sea Nan
        (df['NIVEL_ED'].isin(range(1, 7))) & #nivel educativo (desde primario incompleto hasta universitario completo inclusive)
        (df['CH04'].isin([1, 2])) & #sexo (1=varon, 2=mujer)
        (df['PP04A'].isin([1, 2])) & #el negocio/empresa en la que trabaja es 1=estatal o 2=privada
        (df['PP07H'].isin([1, 2])) & #si por ese trabajo tiene descuento jubilatorio (1=si, 2=no)
        (df['PP07G1'].isin([1, 2])) & #si por ese trabajo tiene vacaciones pagar (1=si, 2=no)
        (df['PP07G2'].isin([1, 2])) & #si por ese trabajo tiene aguinaldo (1=si, 2=no)
        (df['PP07G3'].isin([1, 2])) & #si por ese trabajo tiene dias pagos por enfermedad (1=si, 2=no)
        (df['PP07G4'].isin([1, 2])) & #si por ese trabajo tiene obra social (1=si, 2=no)
        (df['ESTADO'].isin([1, 2])) #condicion de actividad (1=ocupado, 2=desocupado)
    ]

    #Variables predictoras: son variables que se consideran relevantes para predecir el ingreso total
    X = df_validos[['NIVEL_ED', 'CH04', 'CH06', 'PP03D', 'PP3E_TOT', 'PP3F_TOT',
                    'PP04A', 'P21_REAL', 'PP07H', 'PP07G1', 'PP07G2', 'PP07G3', 'PP07G4', 'ESTADO']]
    #Variable objetivo: es la variable que se quiere predecir
    y = np.log(df_validos['P47T_REAL']) #se usa el log para que los ingresos extremos no dominen el modelo

    #Paso las variables categoricas a binarias (OneHotEncoder), dejo las numericas como estan y le pongo el nombre de 'onehot' a la transformacion
    categoricas = ['NIVEL_ED', 'CH04', 'PP04A', 'PP07H', 'PP07G1', 'PP07G2', 'PP07G3', 'PP07G4', 'ESTADO']
    preprocesamiento = ColumnTransformer([('onehot', OneHotEncoder(drop='first'), categoricas)], remainder='passthrough')

    #El pipeline permite encadenar el preprocesamiento
    #Primero: hace el procesamiento de las variables categoricas con el OneHotEncoder
    #Segundo: crea el modelo de regresion con RandomForestRegressor basado en arboles de decisiones multiples
    #El modelo tiene un maximo de 200 arboles, una profundidad de 10, fija la aleatoriedad en 45 y usa todos los nucleos disponibles
    modelo = Pipeline(steps=[
        ('pre', preprocesamiento),
        ('regresor', RandomForestRegressor(n_estimators=200, max_depth=10, random_state=45, n_jobs=-1))
    ])

    #X_train es el conjunto de las variables independientes que se utilizan para entrenar el modelo
    #X_test es el conjunto de las variables independientes que se utilizan para evaluar el modelo
    #y_train son los valores objetivos para entrenar el modelo
    #y_test son los valores objetivos para evaluar el modelo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #20% de los datos son para testear

    modelo.fit(X_train, y_train) #se entrena el modelo

    #Se hacen las predicciones
    y_pred_log = modelo.predict(X_test) #si el ingreso fue 1.000.000, el modelo busca predecir valores alrededor de 13,82 (o sea, su logaritmo)
    y_pred = np.exp(y_pred_log) #se vuelve a la escala original (ingresos totales)
    y_test_exp = np.exp(y_test) #tambien vuelvo a la escala original para comparar los resultados en pesos reales

    #Metricas de evaluacion
    r2 = r2_score(y_test_exp, y_pred) #mide que proporcion de la varianza del ingreso real el modelo logro explicar (0 a 1, siendo 1 perfecto)
    rmse = np.sqrt(mean_squared_error(y_test_exp, y_pred)) #mide el error entre los ingresos reales y los predichos (se equivoca promedio +-200.000)
    mae = mean_absolute_error(y_test_exp, y_pred) #mide el promedio de los errores absolutos (predice ingresos con un error promedio de $110.000)

    print(f"🌲 R²: {r2:.4f}")
    print(f"🌲 RMSE: ${rmse:,.2f}")
    print(f"🌲 MAE: ${mae:,.2f}")

    #Se comparan los resultados reales
    comparacion = pd.DataFrame({
        'Ingreso_real_2024': y_test_exp,
        'Ingreso_predicho': y_pred
    })
    print("\n📋 Comparación de ingresos reales vs predichos:")
    print(comparacion.round(2).head(15))

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test_exp, y=y_pred, alpha=0.4)
    max_val = max(y_test_exp.max(), y_pred.max()) #linea ideal (donde predicho = real)
    plt.plot([0, max_val], [0, max_val], color='red', linestyle='--', label='Predicción perfecta')
    plt.title('Comparación entre ingreso real y predicho')
    plt.xlabel('Ingreso real 2024 ($)')
    plt.ylabel('Ingreso predicho ($)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    #Explicacion:
        #cada punto representa una persona
        #el eje x muestra el ingreso real
        #el eje y muestra el ingreso predicho por el modelo
        #la linea roja punteada indica donde deberian caer los puntos si el modelo fuera perfecto