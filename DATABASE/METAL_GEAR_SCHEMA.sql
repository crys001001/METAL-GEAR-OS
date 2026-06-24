CREATE DATABASE metal_gear_db;
USE metal_gear_db;

CREATE TABLE producao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cor_dado VARCHAR(20),
    numero_lido INT,
    status_peca VARCHAR(15),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);