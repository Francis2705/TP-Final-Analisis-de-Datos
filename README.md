# 📊 Análisis de Ingresos e Indicadores Sociodemográficos en el AMBA

Este proyecto presenta un análisis exhaustivo de los ingresos y condiciones sociodemográficas de los habitantes del Área Metropolitana de Buenos Aires (AMBA), utilizando datos oficiales de la Encuesta Permanente de Hogares (EPH) provistos por el INDEC.

---

## 🔎 Objetivo

Explorar y analizar cómo varían los ingresos ajustados por inflación según distintos factores como el aglomerado, la ocupación, el sexo y el nivel educativo. Se utilizaron técnicas estadísticas y visualización de datos para obtener una mejor comprensión de la realidad social y económica del AMBA.

## 📈 Principales análisis y visualizaciones

- 🔹 Comparación de ingresos promedio por aglomerado.
- 🔹 Ajuste de ingresos por inflación al año 2024.
- 🔹 Visualización geográfica con mapas de calor.
- 🔹 Distribuciones de ingresos por nivel educativo y sexo.
- 🔹 Correlación entre variables clave.
- 🔹 Modelo de regresión para predecir ingresos.

## 🧠 Herramientas utilizadas

- Python
- Pandas / NumPy
- Seaborn / Matplotlib
- GeoPandas / Contextily
- Scikit-learn
- Rich

## 🗂️ Fuente de datos

- **EPH - Encuesta Permanente de Hogares (INDEC)**  
  https://www.indec.gob.ar

---

## 💻 Instalación rápida de dependencias:

```bash
pip install rich
pip install pandas
pip install glob
pip install matplotlib
pip install seaborn
pip install numpy
pip install scikit-learn
pip install contextily
pip install geopandas
```

## 👨‍💻 Ejecución
Primero ejecutar el filtrado de datos (dentro de la carpeta anios):

```bash
python filtrado_datos.py
```

Y luego ejecutar el main:

```bash
python main.py
```
