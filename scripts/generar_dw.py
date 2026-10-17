
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
ENTRADA = BASE / "datos" / "procesado"
SALIDA = BASE / "datos" / "dw"

SALIDA.mkdir(parents=True, exist_ok=True)

COLUMNAS = [
    "Year", "Month", "Reporting_Airline",
    "Origin", "Dest", "DepDelay", "ArrDelay",
    "Cancelled", "Diverted"
]

acumulados = []

archivos = sorted(ENTRADA.glob("vuelos_*_limpio.csv"))

print("=== GENERACION DE DATA WAREHOUSE BTS ===")
print(f"Archivos encontrados: {len(archivos)}")

for archivo in archivos:
    print(f"Procesando: {archivo.name}", flush=True)

    for bloque in pd.read_csv(
        archivo,
        usecols=COLUMNAS,
        chunksize=100000,
        encoding="utf-8"
    ):
        grupo = bloque.groupby(
            [
                "Year", "Month", "Reporting_Airline",
                "Origin", "Dest"
            ],
            dropna=False
        ).agg(
            vuelos=("Cancelled", "size"),
            cancelados=("Cancelled", "sum"),
            desviados=("Diverted", "sum"),
            suma_retraso=("ArrDelay", "sum"),
            vuelos_con_retraso=("ArrDelay", "count")
        ).reset_index()

        acumulados.append(grupo)

datos = pd.concat(acumulados, ignore_index=True)

resultado = datos.groupby(
    [
        "Year", "Month", "Reporting_Airline",
        "Origin", "Dest"
    ],
    as_index=False
).agg(
    vuelos=("vuelos", "sum"),
    cancelados=("cancelados", "sum"),
    desviados=("desviados", "sum"),
    suma_retraso=("suma_retraso", "sum"),
    vuelos_con_retraso=("vuelos_con_retraso", "sum")
)

resultado["retraso_promedio"] = (
    resultado["suma_retraso"]
    / resultado["vuelos_con_retraso"].replace(0, float("nan"))
).round(2)

archivo_salida = SALIDA / "puntualidad_agregada.csv"

resultado.to_csv(
    archivo_salida,
    index=False,
    encoding="utf-8"
)

print("\n=== RESULTADOS ===")
print(f"Filas agregadas: {len(resultado):,}")
print(f"Total de vuelos: {resultado['vuelos'].sum():,}")
print(f"Cancelados: {resultado['cancelados'].sum():,}")
print(f"Desviados: {resultado['desviados'].sum():,}")
print(f"Archivo generado: {archivo_salida}")
print("\n=== PROCESO FINALIZADO ===")
