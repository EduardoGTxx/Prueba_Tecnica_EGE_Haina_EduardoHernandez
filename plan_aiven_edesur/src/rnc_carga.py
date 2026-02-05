import pandas as pd
from sqlalchemy import text

from .db import get_engine
from .rnc_etl import transform_rnc

CSV_PATH = "data/RNC_Contribuyentes_Actualizado_31_Ene_2026.csv"
TABLE_NAME = "rnc_regimenpago"

CREATE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  rnc VARCHAR(20) NOT NULL,
  razon_social VARCHAR(8000) NULL,
  regimen_pago VARCHAR(120) NULL,
  estado VARCHAR(50) NULL,
  actividad_economica VARCHAR(255) NULL,
  fecha DATE NULL,

  UNIQUE KEY uq_rnc (rnc),
  KEY idx_regimen (regimen_pago),
  KEY idx_estado (estado)
);
"""

def main():
    print("Leyendo CSV DGII (RNC)...")
    # encoding típico para archivos con ñ/tildes
    df_raw = pd.read_csv(CSV_PATH, encoding="latin-1")

    print("Transformando...")
    df = transform_rnc(df_raw)

    print("Filas finales:", len(df))
    print(df.head(5))

    if df.empty:
        raise ValueError("El dataframe quedó vacío después de la limpieza. Revisa columnas y formato del CSV.")

    engine = get_engine()

    print("Creando tabla si no existe (con PK)...")
    with engine.begin() as conn:
        conn.execute(text(CREATE_SQL))

    print("Limpiando tabla (TRUNCATE) para recargar desde cero...")
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME};"))

    print("Insertando en MySQL...")
    df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False, chunksize=5000)

    print("Listo. Tabla cargada:", TABLE_NAME)

if __name__ == "__main__":
    main()
