
# Proyecto BTS ECBD

## Inteligencia operativa de puntualidad aérea

**Materia:** ECBD - Preparación de los datos

**Equipo 3**

**Integrantes:**
- Dylan Damián Almaguer Acuña
- Adaia Noemí Rentería Bocanegra
- Jimena Sarahí Rodríguez Zavala

## Descripción

Este proyecto implementa un proceso ETL y un Data Warehouse
para analizar la puntualidad aérea mediante registros del
Bureau of Transportation Statistics (BTS).

El estudio utiliza información de los años 2000 y 2001
para comparar aerolíneas, rutas, cancelaciones, desvíos
y retrasos de vuelos.

## Dataset

Fuente: Bureau of Transportation Statistics (BTS).

Período analizado: 2000-2001.

- 24 archivos ZIP originales.
- 24 archivos CSV preprocesados.
- 11,650,827 registros de vuelos.
- 418,688 cancelaciones.
- 27,163 vuelos desviados.

## Herramientas

- Python 3.11
- pandas
- mysql-connector-python
- MySQL Server 9.7
- MySQL Workbench
- Visual Studio Code
- Git y GitHub

## Proceso ETL

1. Extracción de los archivos ZIP originales.
2. Exploración y selección de columnas relevantes.
3. Estandarización de fechas y formatos.
4. Validación de datos y tratamiento de valores faltantes.
5. Generación de archivos CSV preprocesados.
6. Agrupación de información por fecha, aerolínea y ruta.
7. Carga del conjunto analítico en MySQL.

## Data Warehouse

El proyecto utiliza un esquema estrella compuesto por:

- dim_fecha
- dim_aerolinea
- dim_ruta
- fact_puntualidad

También incluye una tabla de preparación llamada
stg_puntualidad.

El conjunto analítico contiene 97,441 filas agregadas.

## Resultados principales

Se identificaron diferencias en los porcentajes de
cancelación entre los años 2000 y 2001.

También se realizaron consultas SQL para comparar
aerolíneas y encontrar rutas con mayores retrasos.

## Estructura del proyecto

- scripts/: programas Python del proceso ETL.
- sql/: definición del Data Warehouse.
- evidencias/: resultados y capturas del proceso.
- datos/: conjuntos originales y procesados.

## Estado

Proceso ETL y Data Warehouse implementados para
los años 2000 y 2001.

Repositorio en preparación para la publicación
de los conjuntos de datos.
