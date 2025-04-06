# extract/extract_data.py

import pandas as pd

def extract_csv(path: str) -> pd.DataFrame:
    """Carga un archivo CSV desde la ruta especificada."""
    try:
        df = pd.read_csv(path, encoding="utf-8")
        return df
    except Exception as e:
        raise RuntimeError(f"Error al cargar CSV desde {path}: {e}")
