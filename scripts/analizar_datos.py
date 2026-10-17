
from pathlib import Path
from zipfile import ZipFile
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CARPETA = BASE / "datos" / "original" / "2000"

archivos = sorted(CARPETA.glob("*.zip"))

if not archivos:
    raise FileNotFoundError("No hay archivos ZIP del año 2000")

archivo = archivos[0]

print("=== ANALISIS INICIAL BTS ===")
print("Archivo:", archivo.name)

with ZipFile(archivo) as zip_file:
    csvs = [
        nombre for nombre in zip_file.namelist()
        if nombre.lower().endswith(".csv")
        and not nombre.startswith("__MACOSX/")
    ]

    if not csvs:
        raise ValueError("El ZIP no contiene archivos CSV")

    with zip_file.open(csvs[0]) as contenido:
        datos = pd.read_csv(
            contenido,
            encoding="cp1252",
            low_memory=False
        )

print("\nTotal de registros:", len(datos))
print("Total de columnas:", len(datos.columns))

columnas = [
    "Year", "Month", "FlightDate",
    "Reporting_Airline", "Origin", "Dest",
    "DepDelay", "ArrDelay",
    "Cancelled", "Diverted", "Distance"
]

print("\n=== COLUMNAS PRINCIPALES ===")
for columna in columnas:
    if columna in datos.columns:
        print(f"{columna}: disponible")
    else:
        print(f"{columna}: NO ENCONTRADA")

print("\n=== VALORES FALTANTES ===")
disponibles = [c for c in columnas if c in datos.columns]
print(datos[disponibles].isna().sum())

print("\n=== DUPLICADOS EXACTOS ===")
print(datos.duplicated().sum())

print("\n=== ANALISIS FINALIZADO ===")
