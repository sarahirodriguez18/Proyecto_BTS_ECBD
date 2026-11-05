from pathlib import Path
import csv
import json

# Rutas del proyecto
BASE = Path(__file__).resolve().parent.parent
PROCESADO = BASE / "datos" / "procesado"
EVIDENCIAS = BASE / "evidencias"

# División temporal del dataset
CONJUNTOS = {
    "entrenamiento": 2000,
    "prueba": 2001
}

def contar_registros(archivo):
    total = 0

    with archivo.open(
        "r", encoding="latin-1", newline=""
    ) as f:
        lector = csv.reader(f)
        next(lector, None)  # Saltar encabezado

        for fila in lector:
            if fila:
                total += 1

    return total


def preparar():
    resultado = {}

    for nombre, anio in CONJUNTOS.items():
        archivos = sorted(
            PROCESADO.glob(
                f"vuelos_{anio}_??_limpio.csv"
            )
        )

        if len(archivos) != 12:
            raise ValueError(
                f"{nombre}: se esperaban 12 archivos "
                f"y se encontraron {len(archivos)}"
            )

        total = 0
        detalle = []

        for archivo in archivos:
            cantidad = contar_registros(archivo)
            total += cantidad

            detalle.append({
                "archivo": archivo.name,
                "registros": cantidad
            })

        resultado[nombre] = {
            "anio": anio,
            "archivos": len(archivos),
            "registros": total,
            "detalle": detalle
        }

        print(
            f"{nombre}: {len(archivos)} archivos, "
            f"{total:,} registros"
        )

    EVIDENCIAS.mkdir(exist_ok=True)

    salida = EVIDENCIAS / "conjuntos_entrenamiento_prueba.json"

    with salida.open("w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"\nEvidencia guardada en: {salida}")


if __name__ == "__main__":
    preparar()