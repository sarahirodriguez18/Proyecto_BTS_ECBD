
from pathlib import Path
import json
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROCESADOS = BASE / "datos" / "procesado"
REPORTE = BASE / "evidencias" / "reporte_limpieza.json"

reportes = json.loads(REPORTE.read_text(encoding="utf-8"))
archivos = sorted(PROCESADOS.glob("vuelos_*_limpio.csv"))

total_filas = 0
errores = []

print("=== VALIDACION DEL ETL BTS ===")
print("Archivos CSV:", len(archivos))

for archivo in archivos:
    filas = 0

    for bloque in pd.read_csv(
        archivo,
        chunksize=100000,
        encoding="utf-8"
    ):
        filas += len(bloque)

    total_filas += filas
    print(f"{archivo.name}: {filas:,} registros")

total_reporte = sum(
    r["registros_limpios"] for r in reportes
)

print("\n=== RESULTADO GENERAL ===")
print(f"Registros en los CSV: {total_filas:,}")
print(f"Registros del reporte: {total_reporte:,}")

if len(archivos) == len(reportes) == 24 and total_filas == total_reporte:
    print("VALIDACION CORRECTA")
else:
    print("ADVERTENCIA: Revisar archivos o cantidades")
