import pandas as pd
import re
import unicodedata
from datetime import datetime

def clean_column_name(col: str) -> str:
    col = col.strip().lower()
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("ascii")  # Esto quita tildes/ñ
    col = re.sub(r"[^\w\s]", "", col)   # Esto quita símbolos
    col = re.sub(r"\s+", "_", col)      # Esto reemplaza espacios con '_'
    return col

SPANISH_MONTHS = {
    "enero": 1, "ene": 1,
    "febrero": 2, "feb": 2,
    "marzo": 3, "mar": 3,
    "abril": 4, "abr": 4,
    "mayo": 5, "may": 5,
    "junio": 6, "jun": 6,
    "julio": 7, "jul": 7,
    "agosto": 8, "ago": 8,
    "septiembre": 9, "setiembre": 9, "sep": 9, "set": 9,
    "octubre": 10, "oct": 10,
    "noviembre": 11, "nov": 11,
    "diciembre": 12, "dic": 12,
}

def parse_mes(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

    # Si viene como "01" o "1"
    if s.isdigit():
        m = int(s)
        return m if 1 <= m <= 12 else pd.NA

    # Si viene como nombre: "Enero"
    if s in SPANISH_MONTHS:
        return SPANISH_MONTHS[s]

    return pd.NA

def parse_anio(x):
    try:
        y = int(str(x).strip())
        return y if 1900 <= y <= 2100 else pd.NA
    except:
        return pd.NA

def parse_number(x):
    """
    Soporta:
    - "1234.56"
    - "1,234.56"
    - "1.234,56"
    - "1234,56"
    """
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()

    # deja solo dígitos, coma, punto y signo
    s = re.sub(r"[^0-9\.,\-]", "", s)

    if s.count(",") > 0 and s.count(".") > 0:
        # si tiene ambos, asumiremos que es miles con punto y decimales con coma (1.234,56) pero si el formato es 1,234.56, este se invertiría y de igual lo manejamos con heurística por lo que si la última coma está después del último punto entonces coma es decimal si no, punto es decimal
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif s.count(",") > 0 and s.count(".") == 0:
        # solo coma: decimal
        s = s.replace(",", ".")
    # solo punto: decimal

    try:
        return float(s)
    except:
        return pd.NA

def build_periodo(mes, anio):
    try:
        return datetime(int(anio), int(mes), 1).date()
    except:
        return pd.NaT

def transform_edesur(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [clean_column_name(c) for c in df.columns]

    # Columnas después de limpiar: zona, cobros_rd_mm, mes, ano/anio
    if "zona" not in df.columns:
        raise ValueError(f"No encuentro 'zona'. Columnas: {df.columns.tolist()}")
    if "mes" not in df.columns:
        raise ValueError(f"No encuentro 'mes'. Columnas: {df.columns.tolist()}")
    if "ano" not in df.columns and "anio" not in df.columns:
        raise ValueError(f"No encuentro 'ano/anio'. Columnas: {df.columns.tolist()}")

    cobros_candidates = [c for c in df.columns if "cobro" in c]
    if not cobros_candidates:
        raise ValueError(f"No encuentro columna de cobros. Columnas: {df.columns.tolist()}")
    cobros_col = cobros_candidates[0]

    df["zona"] = df["zona"].astype(str).str.strip()
    df["sector"] = df["zona"]

    df["mes"] = df["mes"].apply(parse_mes)

    anio_col = "anio" if "anio" in df.columns else "ano"
    df["anio"] = df[anio_col].apply(parse_anio)

    df["cobros_rd_mm"] = df[cobros_col].apply(parse_number)

    df["periodo"] = df.apply(lambda r: build_periodo(r["mes"], r["anio"]), axis=1)

    print("DEBUG total filas:", len(df))
    print("DEBUG mes NA:", int(df["mes"].isna().sum()))
    print("DEBUG anio NA:", int(df["anio"].isna().sum()))
    print("DEBUG cobros NA:", int(df["cobros_rd_mm"].isna().sum()))
    print("DEBUG periodo NA:", int(pd.isna(df["periodo"]).sum()))
    print("DEBUG ejemplo filas:\n", df[["sector","mes","anio","periodo","cobros_rd_mm"]].head(10))

    df = df[df["sector"] != ""]
    df = df[df["mes"].notna()]
    df = df[df["anio"].notna()]
    df = df[df["periodo"].notna()]
    df = df[df["cobros_rd_mm"].notna()]
    df = df[df["cobros_rd_mm"] >= 0]

    out = df[["sector", "mes", "anio", "periodo", "cobros_rd_mm"]].copy()
    out = out.drop_duplicates(subset=["sector", "mes", "anio"])
    return out


