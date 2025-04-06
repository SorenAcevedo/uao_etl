"""
Módulo principal para ejecutar procesos ETL (Extract, Transform, Load) sobre múltiples datasets.

Este script utiliza un conjunto de configuraciones definidas en `datasets_config` para ejecutar 
los procesos de extracción, transformación y carga de datos. Cada dataset es procesado en paralelo 
utilizando un `ThreadPoolExecutor`, y los logs son almacenados individualmente por dataset.
"""
from extract.extract_data import extract_csv
from load.load_data import save_to_csv
from config.datasets_config import datasets
from config.logger import get_dataset_logger
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os


def run_etl(dataset_name, config):
    """
    Ejecuta el proceso ETL para un dataset específico.

    Args:
        dataset_name (str): Nombre del dataset.
        config (dict): Diccionario de configuración con claves:
            - 'input': ruta del archivo fuente
            - 'output': ruta base del archivo de salida
            - 'transformations': lista de funciones de transformación

    Returns:
        tuple: (nombre del dataset, estado de ejecución)
    """
    logger = get_dataset_logger(dataset_name)
    logger.info(f"Iniciando ETL para: {dataset_name}")

    try:
        # Extracción
        df = extract_csv(config["input"])
        logger.info(f"Datos cargados desde: {config['input']}")

        # Transformación
        for func in config["transformations"]:
            shape_before = df.shape[0]
            df = func(df)
            shape_after = df.shape[0]
            logger.info(f"{func.__name__} - Filas antes: {shape_before}, después: {shape_after}")
            logger.info(f"Transformación aplicada: {func.__name__}")

        # Carga con versionado de nombre de archivo
        processed_dir = "data/processed"
        os.makedirs(processed_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(config["output"]))[0]
        output_path = f"{processed_dir}/{base_name}_{timestamp}.csv"
        save_to_csv(df, output_path)
        logger.info(f"Datos guardados en: {output_path}")
        return (dataset_name, "Éxito")

    except Exception as e:
        logger.error(f"Error procesando dataset '{dataset_name}': {e}")
        return (dataset_name, f"Error: {e}")


def main():
    """
    Ejecuta todos los procesos ETL definidos en `datasets_config` en paralelo.

    Imprime un resumen con el resultado de cada ejecución.
    """
    resumen = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_etl, name, config): name
            for name, config in datasets.items()
        }
        for future in as_completed(futures):
            dataset_name = futures[future]
            try:
                resultado = future.result()
                resumen.append(resultado)
            except Exception as exc:
                resumen.append((dataset_name, f"Error inesperado: {exc}"))

    print("Resumen de ejecución ETL:")
    for nombre, estado in resumen:
        print(f"- {nombre}: {estado}")


if __name__ == "__main__":
    main()
