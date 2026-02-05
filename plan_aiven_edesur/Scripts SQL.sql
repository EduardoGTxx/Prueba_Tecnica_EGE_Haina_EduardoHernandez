----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/* Estos Scripts son para verificar los datos en nuestra db */
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
DESCRIBE fact_edesur_cobros;                                    /* Verificamos los tipos de datos dentro de nuestra tabla */

SELECT COUNT(*) AS Filas FROM fact_edesur_cobros;               /* Verificamos la cantidad de lineas dentro de la tabla */

SELECT DISTINCT sector FROM fact_edesur_cobros ORDER BY sector; /* Verificamos los sectores */

SELECT * FROM fact_edesur_cobros;                               /* Verificamos toda la informacion cargada */
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Vistas por provincia/sector/zona */
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE VIEW VW_Cobros_Distrito AS SELECT sector, periodo, cobros_rd_mm FROM fact_edesur_cobros WHERE sector like '%Distrito%';          /* Vista para ver todas los cobros de la zona Distrito */

CREATE VIEW VW_Cobros_SantoDomingo AS SELECT sector, periodo, cobros_rd_mm FROM fact_edesur_cobros WHERE sector like '%Santo Domingo%'; /* Vista para ver todas los cobros de la zona Santo Domingo */

CREATE VIEW VW_Cobros_SanCristobal AS SELECT sector, periodo, cobros_rd_mm FROM fact_edesur_cobros WHERE sector like '%San Cristobal%'; /* Vista para ver todas los cobros de la zona San Cristobal */

CREATE VIEW VW_Cobros_Bani AS SELECT sector, periodo, cobros_rd_mm FROM fact_edesur_cobros WHERE sector like '%Bani%';                  /* Vista para ver todas los cobros de la zona Bani */

CREATE VIEW VW_Cobros_SanJuan AS SELECT sector, periodo, cobros_rd_mm FROM fact_edesur_cobros WHERE sector like '%San Juan%';           /* Vista para ver todas los cobros de la zona San Juan */

CREATE VIEW VW_Cobros_Barahona AS SELECT sector, periodo, cobros_rd_mm FROM fact_edesur_cobros WHERE sector like '%Barahona%';          /* Vista para ver todas los cobros de la zona Barahona */
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Vistas por Regimen de Pago */
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE VIEW VW_RNC_Regimen_Normal AS SELECT * FROM rnc_regimenpago WHERE regimen_pago = 'NORMAL';      /* Vista para ver todas los contribuyentes de regimen normal */

CREATE VIEW VW_RNC_Regimen_RST AS SELECT * FROM rnc_regimenpago WHERE regimen_pago = 'RST'; /* Vista para ver todas los contribuyentes de regimen RST Itbis */
