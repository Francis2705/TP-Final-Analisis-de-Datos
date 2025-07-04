'''
GENERAL:
        1. Poner todo en un solo archivo y hacer un for(in) para que recorra todos los archivos y filtro las columnas que usaria
        2. Filtro por algomerado, region, etc
        3. Imputar la no respuesta con ponderadores correspondientes
        4. Analizar el no sabe/no responde en los casos del ejemplo de art
acordarse pregunta de la georreferenciacion
'''
# # Filtrar: AMBA (REGIÓN 1, AGLOMERADOS 32 y 33, P21 > 0 y PONDIIO > 0 para que el analisis no se desfaze tanto)
# df_filtrado = df[(df['REGION'] == 1) & (df['AGLOMERADO'].isin([32, 33])) & (df['P21'] > 0) & (df['PONDIIO'] > 0)][['P21', 'PONDIIO']]

# # Calcular media ponderada
# media = np.average(df_filtrado['P21'], weights=df_filtrado['PONDIIO'])

# # Calcular mediana ponderada
# df_sorted = df_filtrado.sort_values('P21')
# cumsum = df_sorted['PONDIIO'].cumsum()
# cutoff = df_sorted['PONDIIO'].sum() / 2
# mediana = df_sorted.loc[cumsum >= cutoff, 'P21'].iloc[0]

# print("📊 Resultados para el 2º trimestre de 2016 (T216)")
# print(f"Media ponderada de P21: ${media:,.2f}")
# print(f"Mediana ponderada de P21: ${mediana:,.2f}")