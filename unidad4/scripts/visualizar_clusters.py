
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

BASE = Path(__file__).resolve().parents[1]
RESULTADOS = BASE / "resultados"
GRAFICAS = BASE / "graficas"
MODELOS = BASE / "modelos"

GRAFICAS.mkdir(parents=True, exist_ok=True)

print("=== VISUALIZACION DE CLUSTERS BTS ===")

# Cargar datos y resultados
datos = pd.read_csv(
    RESULTADOS / "rutas_bts_clusters.csv"
)

metricas = pd.read_csv(
    RESULTADOS / "metricas_clustering.csv"
)

resumen = pd.read_csv(
    RESULTADOS / "resumen_clusters.csv"
)

objetos = joblib.load(
    MODELOS / "kmeans_bts.joblib"
)

escalador = objetos["escalador"]
variables = objetos["variables"]

X = escalador.transform(datos[variables])

mejor_k = int(
    metricas.loc[
        metricas["silhouette"].idxmax(),
        "clusters"
    ]
)

print(f"Registros: {len(datos):,}")
print(f"Mejor numero de clusters: {mejor_k}")

# =====================================
# GRAFICA 1. METODO DEL CODO
# =====================================

plt.figure(figsize=(9, 5))

plt.plot(
    metricas["clusters"],
    metricas["inercia"],
    marker="o",
    linewidth=2,
    color="#2563A6"
)

plt.title("Metodo del codo - K-Means BTS")
plt.xlabel("Numero de clusters (k)")
plt.ylabel("Inercia")

plt.xticks(metricas["clusters"])
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    GRAFICAS / "metodo_codo.png",
    dpi=200
)

plt.close()

print("Grafica 1: Metodo del codo generada")

# =====================================
# GRAFICA 2. COMPARACION DE METRICAS
# =====================================

fig, axes = plt.subplots(
    1, 3, figsize=(15, 5)
)

configuracion = [
    ("silhouette", "Silhouette", "#27876D"),
    ("calinski_harabasz", "Calinski-Harabasz", "#3973AC"),
    ("davies_bouldin", "Davies-Bouldin", "#E5A344")
]

for ax, (columna, titulo, color) in zip(
    axes, configuracion
):
    ax.plot(
        metricas["clusters"],
        metricas[columna],
        marker="o",
        linewidth=2,
        color=color
    )

    ax.set_title(titulo)
    ax.set_xlabel("Numero de clusters")
    ax.set_xticks(metricas["clusters"])
    ax.grid(alpha=0.25)

fig.suptitle(
    "Evaluacion de agrupaciones BTS",
    fontsize=15
)

plt.tight_layout()

plt.savefig(
    GRAFICAS / "comparacion_metricas.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("Grafica 2: Comparacion de metricas generada")

# =====================================
# GRAFICA 3. REDUCCION CON PCA
# =====================================

pca = PCA(
    n_components=2,
    random_state=42
)

componentes = pca.fit_transform(X)

datos["PC1"] = componentes[:, 0]
datos["PC2"] = componentes[:, 1]

varianza = pca.explained_variance_ratio_

print("\n=== RESULTADOS PCA ===")
print(f"Varianza PC1: {varianza[0] * 100:.2f}%")
print(f"Varianza PC2: {varianza[1] * 100:.2f}%")
print(f"Varianza total: {sum(varianza) * 100:.2f}%")

plt.figure(figsize=(10, 7))

grupos = sorted(
    datos["cluster_optimizado"].unique()
)

colores = plt.get_cmap("tab10")

for i, grupo in enumerate(grupos):
    subset = datos[
        datos["cluster_optimizado"] == grupo
    ]

    plt.scatter(
        subset["PC1"],
        subset["PC2"],
        s=14,
        alpha=0.6,
        color=colores(i % 10),
        label=f"Cluster {grupo}: {len(subset)} rutas"
    )

plt.title("Visualizacion PCA de clusters BTS")

plt.xlabel(
    f"Componente principal 1 ({varianza[0]*100:.2f}%)"
)

plt.ylabel(
    f"Componente principal 2 ({varianza[1]*100:.2f}%)"
)

plt.legend()
plt.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    GRAFICAS / "clusters_pca.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

datos.to_csv(
    RESULTADOS / "rutas_bts_pca.csv",
    index=False
)

joblib.dump(
    pca,
    MODELOS / "pca_bts.joblib",
    compress=3
)

print("Grafica 3: Visualizacion PCA generada")

# =====================================
# GRAFICA 4. PERFIL DE LOS GRUPOS
# =====================================

etiquetas = [
    f"Cluster {c}"
    for c in resumen["cluster_optimizado"]
]

x = np.arange(len(etiquetas))
ancho = 0.35

fig, axes = plt.subplots(
    1, 2, figsize=(12, 5)
)

axes[0].bar(
    x,
    resumen["retraso_llegada_promedio"],
    color="#3973AC"
)

axes[0].set_title(
    "Retraso promedio de llegada"
)
axes[0].set_ylabel("Minutos")
axes[0].set_xticks(x)
axes[0].set_xticklabels(etiquetas)

axes[1].bar(
    x,
    resumen["porcentaje_retrasados"],
    color="#E5A344"
)

axes[1].set_title(
    "Porcentaje promedio de retrasados"
)
axes[1].set_ylabel("Porcentaje (%)")
axes[1].set_xticks(x)
axes[1].set_xticklabels(etiquetas)

for ax in axes:
    ax.grid(axis="y", alpha=0.2)

plt.tight_layout()

plt.savefig(
    GRAFICAS / "perfil_clusters.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("Grafica 4: Perfil de clusters generado")

print("\n=== ARCHIVOS GENERADOS ===")

for archivo in sorted(GRAFICAS.glob("*.png")):
    print(archivo.name)

print("\n=== VISUALIZACION FINALIZADA ===")
