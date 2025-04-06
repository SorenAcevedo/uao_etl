# load/load_data.py

import pandas as pd

def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Guarda un DataFrame en un archivo CSV en la ruta especificada."""
    try:
        df.to_csv(output_path, index=False, encoding="utf-8")
    except Exception as e:
        raise RuntimeError(f"Error al guardar CSV en {output_path}: {e}")
