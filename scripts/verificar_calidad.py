
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CARPETA = BASE / "datos" / "procesado"

archivos = sorted(
    CARPETA.glob("vuelos_*_limpio.csv")
)

total = 0
fechas_invalidas = 0
aerolineas_vacias = 0
rutas_invalidas = 0
estados_invalidos = 0
distancias_invalidas = 0
retrasos_llegada_vacios = 0

print("=== VERIFICACION DE CALIDAD BTS ===")

for archivo in archivos:
    print(f"Revisando: {archivo.name}", flush=True)

    for datos in pd.read_csv(
        archivo,
        chunksize=100000,
        encoding="utf-8"
    ):
        total += len(datos)

        fechas = pd.to_datetime(
            datos["FlightDate"],
            errors="coerce"
        )

        fechas_invalidas += int(
            fechas.isna().sum()
        )

        aerolineas_vacias += int(
            datos["Reporting_Airline"].isna().sum()
        )

        rutas_invalidas += int((
            datos["Origin"].isna()
            | datos["Dest"].isna()
            | datos["Origin"].eq(datos["Dest"])
        ).sum())

        estados_invalidos += int((
            ~datos["Cancelled"].isin([0, 1])
            | ~datos["Diverted"].isin([0, 1])
        ).sum())

        distancias_invalidas += int((
            datos["Distance"].isna()
            | datos["Distance"].le(0)
        ).sum())

        retrasos_llegada_vacios += int(
            datos["ArrDelay"].isna().sum()
        )

print("\n=== RESULTADOS ===")
print(f"Registros revisados: {total:,}")
print(f"Fechas invalidas: {fechas_invalidas:,}")
print(f"Aerolineas vacias: {aerolineas_vacias:,}")
print(f"Rutas invalidas: {rutas_invalidas:,}")
print(f"Estados invalidos: {estados_invalidos:,}")
print(f"Distancias invalidas: {distancias_invalidas:,}")
print(
    "Retrasos de llegada sin dato:",
    f"{retrasos_llegada_vacios:,}"
)
print("\n=== VERIFICACION FINALIZADA ===")
