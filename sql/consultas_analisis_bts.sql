
USE dw_bts;

-- 1. Verificar registros de la tabla de hechos
SELECT COUNT(*) AS registros
FROM fact_puntualidad;

-- 2. Comparación de vuelos por año
SELECT
    f.anio,
    SUM(p.vuelos) AS total_vuelos,
    SUM(p.cancelados) AS cancelados,
    SUM(p.desviados) AS desviados,
    ROUND(
        100.0 * SUM(p.cancelados) /
        NULLIF(SUM(p.vuelos), 0), 2
    ) AS porcentaje_cancelacion
FROM fact_puntualidad p
JOIN dim_fecha f
    ON p.fecha_id = f.fecha_id
GROUP BY f.anio
ORDER BY f.anio;

-- 3. Porcentaje de cancelaciones por aerolínea
SELECT
    a.codigo_aerolinea AS aerolinea,
    SUM(p.vuelos) AS total_vuelos,
    SUM(p.cancelados) AS cancelaciones,
    ROUND(
        100.0 * SUM(p.cancelados) /
        NULLIF(SUM(p.vuelos), 0), 2
    ) AS porcentaje_cancelacion
FROM fact_puntualidad p
JOIN dim_aerolinea a
    ON p.aerolinea_id = a.aerolinea_id
GROUP BY a.codigo_aerolinea
ORDER BY porcentaje_cancelacion DESC;

-- 4. Las 10 rutas con mayores retrasos
SELECT
    r.origen,
    r.destino,
    SUM(p.vuelos) AS total_vuelos,
    ROUND(
        SUM(p.suma_retraso) /
        NULLIF(SUM(p.vuelos_con_retraso), 0), 2
    ) AS retraso_promedio_minutos
FROM fact_puntualidad p
JOIN dim_ruta r
    ON p.ruta_id = r.ruta_id
GROUP BY r.origen, r.destino
HAVING SUM(p.vuelos_con_retraso) >= 100
ORDER BY retraso_promedio_minutos DESC
LIMIT 10;
