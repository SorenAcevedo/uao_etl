"""
Módulo de configuración de logging para procesos ETL.

Este módulo proporciona una función para crear un logger personalizado
para cada dataset, que registra los eventos de ejecución en archivos individuales.
"""

import logging
import os


def get_dataset_logger(dataset_name: str) -> logging.Logger:
    """
    Crea o recupera un logger específico para un dataset.

    El logger guarda los mensajes en un archivo dentro de la carpeta 'logs',
    con nombre `etl_<dataset_name>.log`. Si el archivo o la carpeta no existen,
    se crean automáticamente.

    Args:
        dataset_name (str): Nombre del dataset (utilizado para nombrar el archivo log).

    Returns:
        logging.Logger: Logger configurado para el dataset.
    """
    logger = logging.getLogger(dataset_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_path = os.path.join("logs", f"etl_{dataset_name}.log")

    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# Log de ETL para {dataset_name}\n")

    if not logger.handlers:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
