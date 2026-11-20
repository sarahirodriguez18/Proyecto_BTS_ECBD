from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]

train = pd.read_csv(BASE / "datos/entrenamiento.csv")
test = pd.read_csv(BASE / "datos/prueba.csv")

datos = pd.concat([train, test], ignore_index=True)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(
    ["Entrenamiento 2000", "Prueba 2001"],
    [len(train), len(test)],
    color=["#3973AC", "#42A58C"]
)

axes[0].set_title("Division temporal del dataset")
axes[0].set_ylabel("Cantidad de vuelos")

conteo = datos["Retrasado"].value_counts().sort_index()

axes[1].pie(
    conteo.values,
    labels=["Sin retraso significativo", "Retrasado"],
    autopct="%1.2f%%",
    colors=["#42A58C", "#E5A344"],
    startangle=90
)

axes[1].set_title("Distribucion de clases")

plt.tight_layout()

plt.savefig(
    BASE / "graficas/distribucion_datos.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("=== DISTRIBUCION DEL DATASET ===")
print("Entrenamiento:", len(train))
print("Prueba:", len(test))
print(conteo)
print("Grafica generada correctamente")