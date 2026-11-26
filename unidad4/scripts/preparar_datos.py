
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]

ENTRADA = BASE.parent / "unidad3" / "datos"
SALIDA = BASE / "datos"
SALIDA.mkdir(parents=True, exist_ok=True)

print("=== PREPARACION DE DATOS U4 ===", flush=True)

archivos = [
    ENTRADA / "entrenamiento.csv",
    ENTRADA / "prueba.csv"
]

columnas = [
    "Reporting_Airline",
    "Origin",
    "Dest",
    "Distance",
    "DepDelay",
    "ArrDelay"
]

partes = []

for archivo in archivos:
    print(f"Leyendo: {archivo.name}", flush=True)
    datos = pd.read_csv(archivo, usecols=columnas)
    partes.append(datos)

datos = pd.concat(partes, ignore_index=True)

print(f"Registros originales: {len(datos):,}")

datos = datos.dropna(subset=columnas).copy()

# La clase retrasado se calcula únicamente para obtener
# un indicador operativo; no es una etiqueta de entrenamiento.
datos["retrasado_15"] = (
    datos["ArrDelay"] >= 15
).astype(int)

agrupado = datos.groupby(
    ["Reporting_Airline", "Origin", "Dest"],
    as_index=False
).agg(
    vuelos=("ArrDelay", "size"),
    retraso_salida_promedio=("DepDelay", "mean"),
    retraso_llegada_promedio=("ArrDelay", "mean"),
    distancia_promedio=("Distance", "mean"),
    porcentaje_retrasados=("retrasado_15", "mean"),
    desviacion_retraso=("ArrDelay", "std")
)

# Conservar rutas con al menos 20 vuelos observados.
agrupado = agrupado[agrupado["vuelos"] >= 20].copy()

agrupado["porcentaje_retrasados"] *= 100
agrupado["desviacion_retraso"] = (
    agrupado["desviacion_retraso"].fillna(0)
)

agrupado = agrupado.round(4)
agrupado = agrupado.sort_values(
    ["Reporting_Airline", "Origin", "Dest"]
).reset_index(drop=True)

archivo_salida = SALIDA / "rutas_bts_clustering.csv"
agrupado.to_csv(archivo_salida, index=False)

print("\n=== RESULTADOS ===")
print(f"Vuelos analizados: {len(datos):,}")
print(f"Rutas-aerolinea seleccionadas: {len(agrupado):,}")
print(f"Columnas generadas: {len(agrupado.columns)}")

print("\nPrimeros registros:")
print(agrupado.head(5).to_string(index=False))

print("\nArchivo generado:")
print(archivo_salida)

print("\n=== PREPARACION U4 FINALIZADA ===")
