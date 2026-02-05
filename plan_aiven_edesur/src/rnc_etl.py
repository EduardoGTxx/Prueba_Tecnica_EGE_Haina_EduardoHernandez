import pandas as pd
import re
import unicodedata
from datetime import datetime

def _clean_col(s: str) -> str:
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s

def _clean_str(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    return s if s != "" else None

def _clean_rnc(x):
    if pd.isna(x):
        return None
    s = re.sub(r"\D", "", str(x))
    return s if s else None

def _parse_date(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None

def _pick(df_cols, options):
    for c in options:
        if c in df_cols:
            return c
    return None

def transform_rnc(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [_clean_col(c) for c in df.columns]

    rnc_col = _pick(df.columns, [
        "rnc", "rnc_cedula", "rnccedula", "rnc_o_cedula", "rnc_cedula_contribuyente"
    ])

    razon_col = _pick(df.columns, [
        "razon_social", "razon", "nombre_razon_social", "razon_social_nombre",
        "nombre_comercial", "comercial", "nombre"
    ])

    regimen_col = _pick(df.columns, [
        "regimen_pago", "regimen_de_pago", "regimen", "tipo_regimen"
    ])

    estado_col = _pick(df.columns, [
        "estado", "estatus"
    ])

    actividad_col = _pick(df.columns, [
        "actividad_economica", "actividad", "actividad_principal", "actividad_economica_principal"
    ])

    # ✅ CAMBIO: FECHA DE INICIO OPERACIONES -> fecha
    # tras limpiar headers, eso típicamente se vuelve "fecha_de_inicio_operaciones"
    fecha_col = _pick(df.columns, [
        "fecha_de_inicio_operaciones",
        "fecha_inicio_operaciones",
        "fecha_inicio",
        "inicio_operaciones",
        # (fallbacks por si DGII cambia el header)
        "fecha", "fecha_actualizacion", "actualizado_al", "fecha_act", "fecha_de_actualizacion"
    ])

    if not rnc_col:
        raise ValueError(f"No encuentro columna mínima 'rnc'. Columnas: {df.columns.tolist()}")

    out = pd.DataFrame()
    out["rnc"] = df[rnc_col].apply(_clean_rnc)
    out["razon_social"] = df[razon_col].apply(_clean_str) if razon_col else None
    out["regimen_pago"] = df[regimen_col].apply(_clean_str) if regimen_col else None
    out["estado"] = df[estado_col].apply(_clean_str) if estado_col else None
    out["actividad_economica"] = df[actividad_col].apply(_clean_str) if actividad_col else None
    out["fecha"] = df[fecha_col].apply(_parse_date) if fecha_col else None

    out = out[out["rnc"].notna()]
    out = out.drop_duplicates(subset=["rnc"])

    return out
