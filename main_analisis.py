import pandas as pd

df = pd.read_csv('datos_filtrados_amba.txt', sep=';', header=0, low_memory=False)

df.info()