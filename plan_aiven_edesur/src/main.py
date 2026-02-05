import pandas as pd
from sqlalchemy import text

from .db import get_engine
from .etl import transform_edesur

CSV_PATH = "data/edesur.csv"
TABLE_NAME = "fact_edesur_cobros"


def ensure_table(engine):
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        zona VARCHAR(100) NOT NULL,
        mes TINYINT NOT NULL,
        anio SMALLINT NOT NULL,
        periodo DATE NOT NULL,
        cobros_rd_mm DECIMAL(14,2) NOT NULL,
        UNIQUE KEY uq_zona_mes_anio (zona, mes, anio)
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_sql))


def truncate_table(engine):
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME};"))


def main():
    print("Leyendo CSV...")

    # Aqui se especifica el encoding del archivo CSV
    df_raw = pd.read_csv(CSV_PATH, encoding="latin-1")

    print("Transformando data...")
    df = transform_edesur(df_raw)

    print(f"Filas finales: {len(df)}")
    print(df.head(10))

    if df.empty:
        raise ValueError(
            "El dataframe quedó vacío después de la limpieza. "
            "Revisa mes/anio/cobros en el CSV y las reglas de limpieza en etl.py."
        )

    print("Conectando a MySQL (Aiven)...")
    engine = get_engine()

    print("Creando tabla si no existe (con PK)...")
    ensure_table(engine)

    print("Limpiando tabla (TRUNCATE) para recargar desde cero...")
    truncate_table(engine)

    print("Insertando filas en MySQL...")
    df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False, chunksize=5000)

    print("Listo. Tabla cargada:", TABLE_NAME)


if __name__ == "__main__":
    main()
