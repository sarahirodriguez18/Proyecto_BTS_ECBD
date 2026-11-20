from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
ENTRADA = BASE / "datos" / "procesado"
SALIDA = BASE / "unidad3" / "datos"

columnas = [
    "Year", "Month", "FlightDate",
    "Reporting_Airline", "Origin", "Dest",
    "Distance", "DepDelay", "ArrDelay",
    "Cancelled", "Diverted"
]

muestras = []

print("=== PREPARACION DE DATOS U3 ===")

for archivo in sorted(ENTRADA.glob("*.csv")):

    datos = pd.read_csv(archivo, usecols=columnas)

    datos = datos[
        (datos["Cancelled"] == 0) &
        (datos["Diverted"] == 0)
    ].copy()

    datos = datos.dropna(subset=columnas)

    muestra = datos.sample(
        n=min(10000, len(datos)),
        random_state=42
    )

    muestras.append(muestra)

    print(f"{archivo.name}: {len(muestra):,} vuelos")

datos = pd.concat(muestras, ignore_index=True)

datos["Fecha"] = pd.to_datetime(datos["FlightDate"])
datos["DiaSemana"] = datos["Fecha"].dt.dayofweek

datos["Retrasado"] = (
    datos["ArrDelay"] >= 15
).astype(int)

entrenamiento = datos[datos["Year"] == 2000]
prueba = datos[datos["Year"] == 2001]

entrenamiento.to_csv(
    SALIDA / "entrenamiento.csv",
    index=False
)

prueba.to_csv(
    SALIDA / "prueba.csv",
    index=False
)

print("\n=== RESULTADOS ===")
print(f"Total de datos: {len(datos):,}")
print(f"Entrenamiento: {len(entrenamiento):,}")
print(f"Prueba: {len(prueba):,}")

print("\nDistribucion de clases:")
print(datos["Retrasado"].value_counts())

print("\n=== PREPARACION FINALIZADA ===")