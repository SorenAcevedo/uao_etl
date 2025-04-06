"""
Módulo de configuración de datasets

Cada dataset debe de tener en su configuración:
- input (str): indicando la ruta donde está ubicado el archivo
- output (str): indicando el nombre de salida del archivo
- transformations (Dict[func, args]): listado de transformaciones a aplicar
,
filter_by_year_range
Cada transformación debe de tener:
- func (func): función de transformación
- args (Dict[str, Any]): argumentos de la transformación
"""

from transform import (
    transform_cobertura_movil,
    transform_internet_fijo,
    transform_revistas_indexadas,
    transform_grupo_investigacion,
    filter_by_year_range
)

datasets = {
    "cobertura_movil": {
        "input": "data/raw/cobertura_movil.csv",
        "output": "cobertura_movil_procesado",
        "transformations": [
            transform_cobertura_movil,
            filter_by_year_range
        ],
    },
    "internet_fijo": {
        "input": "data/raw/internet_fijo.csv",
        "output": "internet_fijo_procesado",
        "transformations": [
            transform_internet_fijo,
            filter_by_year_range
        ],
    },
    "revistas_indexadas": {
        "input": "data/raw/revistas_indexadas.csv",
        "output": "revistas_indexadas_procesado",
        "transformations": [
            transform_revistas_indexadas,
            filter_by_year_range
        ],
    },
    "grupo_investigacion": {
        "input": "data/raw/grupo_investigacion.csv",
        "output": "grupo_investigacion_procesado",
        "transformations": [
            transform_grupo_investigacion,
            filter_by_year_range
        ],
    },
}
