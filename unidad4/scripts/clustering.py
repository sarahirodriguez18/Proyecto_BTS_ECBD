
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)

BASE = Path(__file__).resolve().parents[1]

ENTRADA = BASE / "datos" / "rutas_bts_clustering.csv"
SALIDA = BASE / "resultados"
MODELOS = BASE / "modelos"

SALIDA.mkdir(parents=True, exist_ok=True)
MODELOS.mkdir(parents=True, exist_ok=True)

print("=== ANALISIS NO SUPERVISADO BTS ===", flush=True)

datos = pd.read_csv(ENTRADA)

variables = [
    "vuelos",
    "retraso_salida_promedio",
    "retraso_llegada_promedio",
    "distancia_promedio",
    "porcentaje_retrasados",
    "desviacion_retraso"
]

X = datos[variables].copy()

print(f"Registros: {len(datos):,}")
print(f"Variables utilizadas: {len(variables)}")

# Normalizar las variables
escalador = StandardScaler()
X_escalado = escalador.fit_transform(X)

# Utilizar la misma muestra para comparar Silhouette
rng = np.random.default_rng(42)

indices = rng.choice(
    len(X_escalado),
    size=min(1200, len(X_escalado)),
    replace=False
)

def evaluar(nombre, k, modelo):
    etiquetas = modelo.labels_

    silhouette = silhouette_score(
        X_escalado[indices],
        etiquetas[indices]
    )

    calinski = calinski_harabasz_score(
        X_escalado,
        etiquetas
    )

    davies = davies_bouldin_score(
        X_escalado,
        etiquetas
    )

    print(f"\n{nombre}", flush=True)
    print(f"Numero de clusters: {k}")
    print(f"Silhouette Score: {silhouette:.4f}")
    print(f"Calinski-Harabasz: {calinski:.4f}")
    print(f"Davies-Bouldin: {davies:.4f}")
    print(f"Inercia: {modelo.inertia_:.4f}")

    return {
        "modelo": nombre,
        "clusters": k,
        "silhouette": silhouette,
        "calinski_harabasz": calinski,
        "davies_bouldin": davies,
        "inercia": modelo.inertia_
    }

# Modelo inicial
print("\n=== MODELO INICIAL ===", flush=True)

inicial = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

inicial.fit(X_escalado)

resultado_inicial = evaluar(
    "K-Means inicial", 3, inicial
)

# Busqueda de cantidad de clusters
print("\n=== OPTIMIZACION ===", flush=True)

resultados = []
modelos = {}

for k in range(2, 7):

    print(f"\nEntrenando K-Means con k={k}", flush=True)

    modelo = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    modelo.fit(X_escalado)

    metricas = evaluar(
        f"K-Means k={k}", k, modelo
    )

    resultados.append(metricas)
    modelos[k] = modelo

tabla = pd.DataFrame(resultados)

# Seleccion del mayor Silhouette
mejor_fila = tabla.loc[
    tabla["silhouette"].idxmax()
]

mejor_k = int(mejor_fila["clusters"])
mejor_modelo = modelos[mejor_k]

print("\n=== MEJOR CONFIGURACION ===")
print(f"Numero de clusters: {mejor_k}")
print(
    f"Silhouette: {mejor_fila['silhouette']:.4f}"
)

# Guardar comparacion
tabla.to_csv(
    SALIDA / "metricas_clustering.csv",
    index=False
)

# Guardar las agrupaciones encontradas
datos["cluster_inicial"] = inicial.labels_
datos["cluster_optimizado"] = mejor_modelo.labels_

datos.to_csv(
    SALIDA / "rutas_bts_clusters.csv",
    index=False
)

# Resumen por cluster optimizado
resumen = datos.groupby(
    "cluster_optimizado"
).agg(
    rutas=("Origin", "size"),
    vuelos_observados=("vuelos", "sum"),
    retraso_salida_promedio=(
        "retraso_salida_promedio", "mean"
    ),
    retraso_llegada_promedio=(
        "retraso_llegada_promedio", "mean"
    ),
    porcentaje_retrasados=(
        "porcentaje_retrasados", "mean"
    ),
    distancia_promedio=(
        "distancia_promedio", "mean"
    )
).round(3)

resumen.to_csv(
    SALIDA / "resumen_clusters.csv"
)

# Guardar los modelos y el escalador
joblib.dump(
    {
        "escalador": escalador,
        "modelo_inicial": inicial,
        "modelo_optimizado": mejor_modelo,
        "variables": variables
    },
    MODELOS / "kmeans_bts.joblib",
    compress=3
)

print("\n=== COMPARACION DE MODELOS ===")
print(tabla.round(4).to_string(index=False))

print("\n=== RESUMEN DE CLUSTERS ===")
print(resumen.to_string())

print("\n=== ARCHIVOS GENERADOS ===")
print("metricas_clustering.csv")
print("rutas_bts_clusters.csv")
print("resumen_clusters.csv")
print("kmeans_bts.joblib")

print("\n=== CLUSTERING FINALIZADO ===")
