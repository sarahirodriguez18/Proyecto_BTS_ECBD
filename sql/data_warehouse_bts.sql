
CREATE DATABASE IF NOT EXISTS dw_bts;

USE dw_bts;

CREATE TABLE IF NOT EXISTS dim_fecha (
    fecha_id INT AUTO_INCREMENT PRIMARY KEY,
    anio SMALLINT NOT NULL,
    mes TINYINT NOT NULL,
    UNIQUE KEY uk_fecha (anio, mes)
);

CREATE TABLE IF NOT EXISTS dim_aerolinea (
    aerolinea_id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_aerolinea VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_ruta (
    ruta_id INT AUTO_INCREMENT PRIMARY KEY,
    origen VARCHAR(10) NOT NULL,
    destino VARCHAR(10) NOT NULL,
    UNIQUE KEY uk_ruta (origen, destino)
);

CREATE TABLE IF NOT EXISTS fact_puntualidad (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fecha_id INT NOT NULL,
    aerolinea_id INT NOT NULL,
    ruta_id INT NOT NULL,
    vuelos INT NOT NULL,
    cancelados INT NOT NULL,
    desviados INT NOT NULL,
    suma_retraso DOUBLE,
    vuelos_con_retraso INT,
    FOREIGN KEY (fecha_id)
        REFERENCES dim_fecha(fecha_id),
    FOREIGN KEY (aerolinea_id)
        REFERENCES dim_aerolinea(aerolinea_id),
    FOREIGN KEY (ruta_id)
        REFERENCES dim_ruta(ruta_id),
    UNIQUE KEY uk_grupo (
        fecha_id, aerolinea_id, ruta_id
    )
);


USE dw_bts;

CREATE TABLE IF NOT EXISTS stg_puntualidad (
    Year SMALLINT,
    Month TINYINT,
    Reporting_Airline VARCHAR(20),
    Origin VARCHAR(10),
    Dest VARCHAR(10),
    vuelos INT,
    cancelados INT,
    desviados INT,
    suma_retraso DOUBLE,
    vuelos_con_retraso INT,
    retraso_promedio DOUBLE
);
