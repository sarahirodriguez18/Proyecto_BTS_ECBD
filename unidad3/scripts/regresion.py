from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
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
y_train = train["ArrDelay"]

X_test = test[variables]
y_test = test["ArrDelay"]

resultados = []
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
        "MAE": mean_absolute_error(y_test, pred),
        "RMSE": np.sqrt(
            mean_squared_error(y_test, pred)
        ),
        "R2": r2_score(y_test, pred)
    }

    resultados.append(metricas)
    modelos[nombre] = modelo

    print("\n", nombre)
    print(f"MAE: {metricas['MAE']:.4f}")
    print(f"RMSE: {metricas['RMSE']:.4f}")
    print(f"R2: {metricas['R2']:.4f}")

print("=== MODELOS DE REGRESION BTS ===")
print("Entrenamiento:", len(X_train))
print("Prueba:", len(X_test))

print("\nEntrenando regresion lineal...", flush=True)

lineal = crear_pipeline(LinearRegression())
lineal.fit(X_train, y_train)

evaluar("Regresion lineal", lineal)

print("\nEntrenando Random Forest inicial...", flush=True)

rf = crear_pipeline(
    RandomForestRegressor(
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

mejor_mae = float("inf")
mejores_parametros = None

for profundidad in [12, 16]:
    parametros = {
        "n_estimators": 40,
        "max_depth": profundidad,
        "min_samples_leaf": 3,
        "max_features": 0.5,
        "random_state": 42,
        "n_jobs": -1
    }

    candidato = crear_pipeline(
        RandomForestRegressor(**parametros)
    )

    candidato.fit(
        ajuste[variables],
        ajuste["ArrDelay"]
    )

    pred = candidato.predict(validacion[variables])

    mae = mean_absolute_error(
        validacion["ArrDelay"], pred
    )

    print(
        f"Profundidad {profundidad}: "
        f"MAE validacion = {mae:.4f}",
        flush=True
    )

    if mae < mejor_mae:
        mejor_mae = mae
        mejores_parametros = parametros

print("Mejores parametros:", mejores_parametros)

optimizado = crear_pipeline(
    RandomForestRegressor(**mejores_parametros)
)

optimizado.fit(X_train, y_train)

evaluar("Random Forest optimizado", optimizado)

tabla = pd.DataFrame(resultados)

tabla.to_csv(
    BASE / "resultados/metricas_regresion.csv",
    index=False
)

joblib.dump(
    optimizado,
    BASE / "modelos/regresion_optimizada.joblib",
    compress=3
)

print("\n=== COMPARACION FINAL ===")
print(tabla.round(4).to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, metrica in zip(axes, ["MAE", "RMSE", "R2"]):
    ax.bar(
        tabla["Modelo"],
        tabla[metrica],
        color=["#3973AC", "#42A58C", "#E5A344"]
    )
    ax.set_title(metrica)
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.2)

fig.suptitle("Comparacion de modelos de regresion")
plt.tight_layout()

plt.savefig(
    BASE / "graficas/comparacion_regresion.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\n=== REGRESION FINALIZADA ===")