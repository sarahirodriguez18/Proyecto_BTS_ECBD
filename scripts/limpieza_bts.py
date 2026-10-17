
from pathlib import Path
from zipfile import ZipFile
import csv
import json
import re
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
ORIGEN = BASE / "datos" / "original"
DESTINO = BASE / "datos" / "procesado"
EVIDENCIAS = BASE / "evidencias"

DESTINO.mkdir(parents=True, exist_ok=True)
EVIDENCIAS.mkdir(parents=True, exist_ok=True)

COLUMNAS = [
    "Year", "Month", "FlightDate",
    "Reporting_Airline", "Flight_Number_Reporting_Airline",
    "Origin", "Dest", "DepDelay", "ArrDelay",
    "Cancelled", "Diverted", "Distance"
]

CLAVE = [
    "FlightDate", "Reporting_Airline",
    "Flight_Number_Reporting_Airline", "Origin", "Dest"
]

def procesar(archivo):
    print(f"\nProcesando: {archivo.name}", flush=True)

    coincidencia = re.search(r"_(\d{4})_(\d{1,2})\.zip$", archivo.name)
    if not coincidencia:
        print("Nombre no reconocido. Se omite.")
        return None

    anio, mes = map(int, coincidencia.groups())
    salida = DESTINO / f"vuelos_{anio}_{mes:02d}_limpio.csv"

    estadisticas = {
        "archivo": archivo.name,
        "registros_originales": 0,
        "registros_limpios": 0,
        "duplicados_eliminados": 0,
        "registros_invalidos": 0,
        "vuelos_cancelados": 0,
        "vuelos_desviados": 0
    }

    claves_vistas = set()
    primera_escritura = True

    with ZipFile(archivo) as comprimido:
        csvs = [
            nombre for nombre in comprimido.namelist()
            if nombre.lower().endswith(".csv")
            and not nombre.startswith("__MACOSX/")
        ]

        if len(csvs) != 1:
            raise ValueError(
                f"Se esperaba un CSV en {archivo.name}; "
                f"se encontraron {len(csvs)}"
            )

        with comprimido.open(csvs[0]) as contenido:
            bloques = pd.read_csv(
                contenido,
                encoding="cp1252",
                chunksize=50000,
                low_memory=False
            )

            for bloque in bloques:
                estadisticas["registros_originales"] += len(bloque)

                faltantes = [
                    col for col in COLUMNAS
                    if col not in bloque.columns
                ]
                if faltantes:
                    raise ValueError(f"Faltan columnas: {faltantes}")

                datos = bloque[COLUMNAS].copy()

                datos["FlightDate"] = pd.to_datetime(
                    datos["FlightDate"], errors="coerce"
                )

                numericas = [
                    "Year", "Month",
                    "Flight_Number_Reporting_Airline",
                    "DepDelay", "ArrDelay",
                    "Cancelled", "Diverted", "Distance"
                ]

                for col in numericas:
                    datos[col] = pd.to_numeric(
                        datos[col], errors="coerce"
                    )

                for col in ["Reporting_Airline", "Origin", "Dest"]:
                    datos[col] = (
                        datos[col]
                        .astype("string")
                        .str.strip()
                        .str.upper()
                    )

                validos = (
                    datos["FlightDate"].notna()
                    & datos["FlightDate"].dt.year.eq(anio)
                    & datos["FlightDate"].dt.month.eq(mes)
                    & datos["Reporting_Airline"].notna()
                    & datos["Origin"].notna()
                    & datos["Dest"].notna()
                    & datos["Cancelled"].isin([0, 1])
                    & datos["Diverted"].isin([0, 1])
                    & datos["Distance"].ge(0)
                )

                estadisticas["registros_invalidos"] += (
                    (~validos).sum().item()
                )

                datos = datos.loc[validos].copy()

                # Eliminar solamente duplicados exactos.
                # No usar CLAVE para deduplicar, ya que pueden
                # existir vuelos distintos con igual identificación.
                datos = datos.drop_duplicates()

                # Evitar duplicados idénticos entre bloques
                conservados = []
                for fila in datos.itertuples(index=False, name=None):
                    clave = tuple(
                        None if pd.isna(v) else v for v in fila
                    )
                    if clave in claves_vistas:
                        conservados.append(False)
                    else:
                        claves_vistas.add(clave)
                        conservados.append(True)

                estadisticas["duplicados_eliminados"] += (
                    len(datos) - sum(conservados)
                )

                datos = datos.loc[conservados].copy()

                estadisticas["vuelos_cancelados"] += int(
                    datos["Cancelled"].eq(1).sum()
                )
                estadisticas["vuelos_desviados"] += int(
                    datos["Diverted"].eq(1).sum()
                )

                datos["FlightDate"] = (
                    datos["FlightDate"].dt.strftime("%Y-%m-%d")
                )

                datos.to_csv(
                    salida,
                    mode="w" if primera_escritura else "a",
                    index=False,
                    header=primera_escritura,
                    encoding="utf-8",
                    quoting=csv.QUOTE_MINIMAL
                )

                primera_escritura = False
                estadisticas["registros_limpios"] += len(datos)

    print(
        f"Originales: {estadisticas['registros_originales']:,} | "
        f"Limpios: {estadisticas['registros_limpios']:,}",
        flush=True
    )

    return estadisticas


def main():
    archivos = sorted(ORIGEN.rglob("*.zip"))
    print(f"ZIP encontrados: {len(archivos)}")

    reportes = []

    for archivo in archivos:
        try:
            resultado = procesar(archivo)
            if resultado is not None:
                reportes.append(resultado)
        except Exception as error:
            print(f"ERROR en {archivo.name}: {error}")
            raise

    reporte = EVIDENCIAS / "reporte_limpieza.json"
    reporte.write_text(
        json.dumps(reportes, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\n=== ETL FINALIZADO ===")
    print(f"Archivos procesados: {len(reportes)}")
    print(f"Reporte generado: {reporte}")


if __name__ == "__main__":
    main()
