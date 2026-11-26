

\# Unidad 4 - Analisis No Supervisado BTS



\## Caso practico

Inteligencia operativa de puntualidad aerea.



\## Objetivo

Identificar grupos de rutas y aerolineas que presentan

comportamientos operativos similares mediante K-Means

y visualizar las agrupaciones utilizando PCA.



\## Dataset

Fuente: Bureau of Transportation Statistics (BTS).

Periodo: 2000-2001.



Se reutilizaron 240,000 registros de la Unidad 3.

Se generaron 3,363 combinaciones de aerolinea y ruta

con al menos 20 vuelos observados.



\## Algoritmos

\- K-Means: agrupacion de rutas.

\- PCA: reduccion de dimensionalidad para visualizacion.



\## Evaluacion

Se utilizaron:

\- Silhouette Score.

\- Calinski-Harabasz Index.

\- Davies-Bouldin Index.

\- Inercia.



Se compararon configuraciones de 2 a 6 clusters.



\## Resultados



Modelo inicial: K-Means con 3 clusters.

Silhouette inicial: 0.2137.



Modelo seleccionado: K-Means con 2 clusters.

Silhouette final: 0.3170.



Cluster 0:

\- 1,303 rutas-aerolinea.

\- Retraso promedio de llegada: 13.927 minutos.

\- Porcentaje promedio de retrasados: 29.049%.



Cluster 1:

\- 2,060 rutas-aerolinea.

\- Retraso promedio de llegada: 3.328 minutos.

\- Porcentaje promedio de retrasados: 16.602%.



\## Resultados PCA

\- Componente principal 1: 51.92%.

\- Componente principal 2: 19.66%.

\- Varianza explicada acumulada: 71.59%.



PCA se utiliza para visualizar los grupos identificados

por K-Means y no para entrenar el modelo de clustering.



\## Ejecucion



Desde la carpeta principal del proyecto:



1\. python -m pip install -r unidad4/requirements.txt

2\. python unidad4/scripts/preparar\_datos.py

3\. python unidad4/scripts/clustering.py

4\. python unidad4/scripts/visualizar\_clusters.py



\## Archivos principales

\- datos/: dataset transformado.

\- scripts/: programas Python.

\- modelos/: modelos K-Means y PCA.

\- resultados/: metricas y agrupaciones.

\- graficas/: visualizaciones.



\## Repositorio

https://github.com/sarahirodriguez18/Proyecto\_BTS\_ECBD



