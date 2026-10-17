
from pathlib import Path
from getpass import getpass
import mysql.connector
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
ARCHIVO = BASE / "datos" / "dw" / "puntualidad_agregada.csv"

COLUMNAS = [
    "Year", "Month", "Reporting_Airline",
    "Origin", "Dest", "vuelos",
    "cancelados", "desviados",
    "suma_retraso", "vuelos_con_retraso",
    "retraso_promedio"
]

def main():
    if not ARCHIVO.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo: {ARCHIVO}"
        )

    print("=== IMPORTACION BTS A MYSQL ===")

    usuario = input("Usuario MySQL [root]: ").strip() or "root"
    password = getpass("Contrasena MySQL: ")

    conexion = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=usuario,
        password=password,
        database="dw_bts",
        connection_timeout=15
    )

    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM stg_puntualidad"
        )
        existentes = cursor.fetchone()[0]

        if existentes != 0:
            raise RuntimeError(
                f"La tabla ya contiene {existentes} registros. "
                "No se importara otra vez para evitar duplicados."
            )

        columnas_sql = ", ".join(
            f"`{col}`" for col in COLUMNAS
        )

        marcadores = ", ".join(["%s"] * len(COLUMNAS))

        consulta = (
            f"INSERT INTO stg_puntualidad "
            f"({columnas_sql}) "
            f"VALUES ({marcadores})"
        )

        total = 0

        for bloque in pd.read_csv(
            ARCHIVO,
            chunksize=1000,
            encoding="utf-8",
            usecols=COLUMNAS
        ):
            registros = []

            for fila in bloque[COLUMNAS].itertuples(
                index=False, name=None
            ):
                registros.append(
                    tuple(
                        None if pd.isna(valor)
                        else valor.item()
                        if hasattr(valor, "item")
                        else valor
                        for valor in fila
                    )
                )

            cursor.executemany(consulta, registros)
            conexion.commit()

            total += len(registros)

            print(
                f"Registros importados: {total:,}",
                flush=True
            )

        cursor.execute(
            "SELECT COUNT(*) FROM stg_puntualidad"
        )

        verificados = cursor.fetchone()[0]

        print("\n=== IMPORTACION FINALIZADA ===")
        print(f"Registros importados: {total:,}")
        print(f"Registros en MySQL: {verificados:,}")

        if total == 97441 and verificados == total:
            print("VALIDACION CORRECTA")
        else:
            print(
                "ADVERTENCIA: revisar cantidad importada"
            )

    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
