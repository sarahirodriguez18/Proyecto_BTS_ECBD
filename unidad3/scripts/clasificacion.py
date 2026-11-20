from pathlib import Path
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

BASE = Path(__file__).resolve().parents[1]

train = pd.read_csv(BASE / "datos/entrenamiento.csv")
test = pd.read_csv(BASE / "datos/prueba.csv")

numericas = [
    "Month", "DiaSemana", "Distance", "DepDelay"
]

categoricas = [
    "Reporting_Airline", "Origin", "Dest"
]

variables = numericas + categoricas

X_train = train[variables]
y_train = train["Retrasado"]

X_test = test[variables]
y_test = test["Retrasado"]

resultados = []
predicciones = {}
modelos = {}

def crear_pipeline(algoritmo):
    preprocesador = ColumnTransformer([
        ("num", StandardScaler(), numericas),
        ("cat", OneHotEncoder(
            handle_unknown="ignore"
        ), categoricas)
    ])

    return Pipeline([
        ("preprocesador", preprocesador),
        ("modelo", algoritmo)
    ])

def evaluar(nombre, modelo):

    pred = modelo.predict(X_test)

    metricas = {
        "Modelo": nombre,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(
            y_test, pred, zero_division=0
        ),
        "Recall": recall_score(
            y_test, pred, zero_division=0
        ),
        "F1": f1_score(
            y_test, pred, zero_division=0
        )
    }

    resultados.append(metricas)
    predicciones[nombre] = pred
    modelos[nombre] = modelo

    print("\n", nombre)

    for metrica, valor in metricas.items():
        if metrica != "Modelo":
            print(f"{metrica}: {valor:.4f}")

print("=== MODELOS DE CLASIFICACION BTS ===")
print("Entrenamiento:", len(X_train))
print("Prueba:", len(X_test))

print("\nEntrenando regresion logistica...", flush=True)

logistica = crear_pipeline(
    LogisticRegression(max_iter=1000)
)

logistica.fit(X_train, y_train)

evaluar("Regresion logistica", logistica)

print("\nEntrenando Random Forest inicial...", flush=True)

rf = crear_pipeline(
    RandomForestClassifier(
        n_estimators=30,
        max_depth=10,
        max_features=0.5,
        random_state=42,
        n_jobs=-1
    )
)

rf.fit(X_train, y_train)

evaluar("Random Forest inicial", rf)

print("\n=== OPTIMIZACION TEMPORAL ===")

ajuste = train[train["Month"] <= 9]
validacion = train[train["Month"] >= 10]

mejor_f1 = -1
mejores_parametros = None

for profundidad in [12, 16]:

    parametros = {
        "n_estimators": 40,
        "max_depth": profundidad,
        "min_samples_leaf": 3,
        "max_features": 0.5,
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1
    }

    candidato = crear_pipeline(
        RandomForestClassifier(**parametros)
    )

    candidato.fit(
        ajuste[variables],
        ajuste["Retrasado"]
    )

    pred = candidato.predict(
        validacion[variables]
    )

    f1 = f1_score(
        validacion["Retrasado"],
        pred,
        zero_division=0
    )

    print(
        f"Profundidad {profundidad}: "
        f"F1 validacion = {f1:.4f}",
        flush=True
    )

    if f1 > mejor_f1:
        mejor_f1 = f1
        mejores_parametros = parametros

print("Mejores parametros:", mejores_parametros)

optimizado = crear_pipeline(
    RandomForestClassifier(**mejores_parametros)
)

optimizado.fit(X_train, y_train)

evaluar("Random Forest optimizado", optimizado)

tabla = pd.DataFrame(resultados)

tabla.to_csv(
    BASE / "resultados/metricas_clasificacion.csv",
    index=False
)

joblib.dump(
    optimizado,
    BASE / "modelos/clasificacion_optimizada.joblib",
    compress=3
)

print("\n=== COMPARACION FINAL ===")
print(tabla.round(4).to_string(index=False))

print("\n=== REPORTE DEL MODELO OPTIMIZADO ===")

print(classification_report(
    y_test,
    predicciones["Random Forest optimizado"],
    target_names=["Sin retraso", "Retrasado"],
    zero_division=0
))

# Grafica comparativa

ax = tabla.set_index("Modelo").plot(
    kind="bar",
    figsize=(12, 6),
    color=[
        "#3973AC",
        "#42A58C",
        "#E5A344",
        "#8766B5"
    ]
)

ax.set_title("Comparacion de modelos de clasificacion")
ax.set_ylabel("Valor de la metrica")
ax.set_ylim(0, 1)
ax.tick_params(axis="x", rotation=15)
ax.grid(axis="y", alpha=0.2)

plt.tight_layout()

plt.savefig(
    BASE / "graficas/comparacion_clasificacion.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

# Matrices de confusion

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for ax, (nombre, pred) in zip(
    axes, predicciones.items()
):

    matriz = confusion_matrix(y_test, pred)

    sns.heatmap(
        matriz,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Sin retraso", "Retrasado"],
        yticklabels=["Sin retraso", "Retrasado"],
        ax=ax
    )

    ax.set_title(nombre)
    ax.set_xlabel("Prediccion")
    ax.set_ylabel("Valor real")

plt.tight_layout()

plt.savefig(
    BASE / "graficas/matrices_confusion.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\n=== CLASIFICACION FINALIZADA ===")