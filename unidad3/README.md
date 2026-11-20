\# Unidad 3 - Analisis Supervisado BTS



\## Equipo 3

Inteligencia operativa de puntualidad aerea.



\## Objetivo

Predecir los minutos de retraso de llegada y

clasificar los vuelos segun su puntualidad.



\## Dataset

Bureau of Transportation Statistics (BTS).

Periodo: 2000-2001.



\- Entrenamiento: 120,000 registros del 2000.

\- Prueba: 120,000 registros del 2001.

\- Total: 240,000 registros.



\## Modelos de regresion



| Modelo | MAE | RMSE | R2 |

|---|---:|---:|---:|

| Regresion lineal | 9.5134 | 13.6828 | 0.8190 |

| Random Forest inicial | 9.3420 | 14.7799 | 0.7888 |

| Random Forest optimizado | 9.3029 | 14.4025 | 0.7995 |



\## Modelos de clasificacion



| Modelo | Accuracy | Precision | Recall | F1 |

|---|---:|---:|---:|---:|

| Regresion logistica | 0.9117 | 0.8443 | 0.6638 | 0.7432 |

| Random Forest inicial | 0.9146 | 0.8595 | 0.6650 | 0.7498 |

| Random Forest optimizado | 0.8915 | 0.7060 | 0.7473 | 0.7261 |



\## Resultados



Random Forest optimizado obtuvo el menor MAE.

La regresion lineal obtuvo el mejor RMSE y R2.

Random Forest inicial obtuvo el mejor F1 en clasificacion.

Random Forest optimizado obtuvo el mayor Recall.



\## Instrucciones de ejecucion



Desde la carpeta principal del proyecto:



1\. pip install -r unidad3/requirements.txt

2\. python unidad3/scripts/preparar\_datos.py

3\. python unidad3/scripts/regresion.py

4\. python unidad3/scripts/clasificacion.py

5\. python unidad3/scripts/distribucion\_datos.py



\## Herramientas



\- Python

\- Pandas

\- Scikit-learn

\- Matplotlib

\- Seaborn

\- Joblib

\- Git y GitHub

