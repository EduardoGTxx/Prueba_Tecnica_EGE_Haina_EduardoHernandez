import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env.txt") # Se busca el archivo .env.txt, este contiene los datos de conexion a la db en Aiven
load_dotenv(ENV_PATH)


def get_engine():
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    db = os.getenv("MYSQL_DB")

    if not all([host, port, user, password, db]):
        raise ValueError("Faltan variables en el .env (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)") # Verifica que todos los datos esten digitados

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url)
    return engine

