
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
ORIGINAL = BASE / "datos" / "original"

archivos = sorted(ORIGINAL.rglob("*.zip"))

print("=== EXPLORACION DEL DATASET BTS ===")
print(f"Total de archivos ZIP: {len(archivos)}")

for archivo in archivos:
    print(f"\nArchivo: {archivo.name}")

    try:
        with ZipFile(archivo) as zip_file:
            csvs = [
                nombre for nombre in zip_file.namelist()
                if nombre.lower().endswith(".csv")
                and not nombre.startswith("__MACOSX/")
            ]

            if not csvs:
                print("No se encontraron archivos CSV.")
                continue

            for nombre_csv in csvs:
                with zip_file.open(nombre_csv) as contenido:
                    datos = pd.read_csv(
                        contenido,
                        nrows=5,
                        encoding="cp1252"
                    )

                print(f"Columnas encontradas: {len(datos.columns)}")
                print("Nombres de columnas:")
                print(datos.columns.tolist())

                print("\nPrimeras 3 filas:")
                print(datos.head(3).to_string(index=False))

    except (BadZipFile, OSError, ValueError, UnicodeError) as error:
        print(f"ERROR: {error}")

print("\n=== EXPLORACION FINALIZADA ===")
