# 📊 Proyecto Final – Curso de ETL y Ciencia de Datos

## 👥 Participantes:
- Juan José Bonilla Pinzón.
- Juan Manuel García Ortiz.
- Ricardo Muñoz Bocanegra.
- Soren Fabricius Acevedo Azuero.

## 🌍 Contexto del Proyecto

### ❓ Descripción del problema:
En la era digital, el acceso a internet es fundamental para el desarrollo y la difusión del conocimiento científico. En Colombia, la cobertura de internet varía significativamente entre los diferentes departamentos, lo que podría afectar la producción científica y el reconocimiento de revistas y grupos de investigación. 

Este proyecto tiene como objetivo analizar la relación entre la cobertura de internet y la producción científica en los departamentos de Colombia, utilizando datos de acceso a internet, revistas indexadas y grupos de investigación.

### 🎯 Justificación del proyecto:
El acceso a internet es una herramienta clave para la comunicación y el intercambio de información científica. Sin embargo, la desigualdad en la cobertura de internet puede limitar las oportunidades de los investigadores en regiones con menor acceso. Analizar esta relación permitirá identificar áreas que podrían beneficiarse de inversiones en infraestructura de internet, promoviendo así un desarrollo científico más equitativo en todo el país.

## 📂 Estructura del Proyecto  

```
uao_etl/
│── 📄 pipeline.py           # Script principal del pipeline ETL
│── 📂 data/                 # Datos del proyecto
│   ├── 📂 raw/              # Datos en bruto sin procesar
│   ├── 📂 processed/        # Datos transformados
│── 📂 extract/              # Módulos de extracción de datosrevistas y grupos
│── 📂 transform/            # Módulos de transformación de datos
│── 📂 load/                 # Módulos de carga de datos
│── 📂 config/               # Configuración
│── 📂 logs/                # Logs del proceso ETL

```


## 📊 Identificación Inicial de Fuentes

| # | 📌 Fuente de Datos | 🌐 Origen | 📄 Tipo | 📦 Volumen |
|---|---------------|--------|------|---------|
| 1 | Cobertura móvil por tecnología, departamento y municipio | Datos Abiertos Colombia | CSV, API | ~41 MB |
| 2 | Internet fijo: Accesos por tecnología y segmento | Datos Abiertos Colombia | CSV, API | ~340 MB |
| 3 | Revistas Indexadas (Índice Nacional Publindex 2017-2020) | Datos Abiertos Colombia | CSV, XML | ~2 MB |
| 4 | Grupos de Investigación Reconocidos | Datos Abiertos Colombia | CSV, API | ~10 MB |

Estos datasets proporcionarán la base necesaria para realizar el análisis exploratorio, la transformación y la modelación de los datos. Al combinar la información sobre la cobertura de internet con los datos de producción científica, esperamos identificar correlaciones y patrones que puedan informar políticas públicas y estrategias de desarrollo.

Este proyecto busca relacionar la cobertura de internet en Colombia (móvil y fija) con la producción científica. Para ello, se realiza un proceso de ETL sobre cuatro datasets:

- **Cobertura de internet fijo**: Contiene información sobre la penetración del servicio de internet fijo en distintos municipios del país.
- **Cobertura de internet móvil**: Presenta datos sobre la disponibilidad de internet móvil en diferentes regiones.
- **Revistas indexadas**: Incluye información sobre publicaciones académicas reconocidas en Colombia.
- **Grupos de investigación en Colombia**: Base de datos con los grupos de investigación registrados en el país.

El propósito del notebook es limpiar, transformar e integrar estos datos para su análisis.

---

## 1. Carga de Datos
Los datos son cargados desde archivos CSV utilizando la biblioteca `pandas`. Esto permite manipular grandes volúmenes de datos de manera eficiente.

```python
import pandas as pd
import numpy as np
from google.colab import files

# Cargamos las librerías necesarias
uploaded = files.upload()
filename = list(uploaded.keys())[0]
df = pd.read_csv(filename)
```

Se realiza una inspección inicial para verificar los tipos de datos, valores faltantes y detectar posibles inconsistencias:

```python
df.dtypes
df.isnull().sum()
df.describe()
```

---

## 2. Transformaciones por Dataset

### a) Cobertura de Internet Fijo

**Objetivo:** Estandarizar la información geográfica y eliminar datos innecesarios.

- Se identificaron valores faltantes en la columna `COD MUNICIPIO`. Para evitar errores en el análisis, estos valores se completaron basándose en registros similares.
- Se eliminaron columnas irrelevantes como `CABECERA MUNICIPAL`, que no aportaban valor analítico.
- Se normalizaron los nombres de municipios y departamentos eliminando tildes y espacios innecesarios para evitar inconsistencias al hacer joins con otros datasets.

```python
df_fijo['MUNICIPIO'] = df_fijo['MUNICIPIO'].str.lower().str.replace(r'\s+', ' ', regex=True)
```

### b) Cobertura de Internet Móvil

**Objetivo:** Limpiar y consolidar la información para reflejar correctamente la cobertura móvil en cada municipio.

- Se eliminaron registros duplicados para evitar redundancias en el análisis.
- En algunos municipios había registros múltiples con diferentes valores de cobertura. Para solucionar esto, se calculó un promedio de la cobertura por municipio y departamento.

```python
df_movil = df_movil.groupby(['COD_DEPARTAMENTO', 'COD MUNICIPIO']).mean().reset_index()
```

### c) Revistas Indexadas

**Objetivo:** Completar información faltante en la ubicación de las revistas indexadas.

- Se detectaron registros donde `DEP_REV_IN` contenía "bogota" pero el código de departamento estaba ausente. Como Bogotá tiene código `11`, se imputó este valor para garantizar una correcta asignación geográfica.
- Se normalizaron nombres de departamentos y ciudades para alinearlos con otros datasets.

```python
df_revistas.loc[df_revistas['DEP_REV_IN'].str.contains('bogota', case=False, na=False), 'COD_DEPARTAMENTO'] = 11
```

### d) Grupos de Investigación

**Objetivo:** Facilitar la integración con otras bases de datos.

- Se estandarizaron los nombres de los departamentos para hacer coincidir esta información con los otros datasets.
- Se eliminaron columnas no relevantes que no contribuían a los análisis posteriores.

---

## 3. Integración de Datos

Para permitir la análisis conjunto de estos datos, se unieron los distintos datasets utilizando claves comunes:

```python
df_final = df_fijo.merge(df_movil, on=['COD_DEPARTAMENTO', 'COD MUNICIPIO'], how='inner')
df_final = df_final.merge(df_revistas, on=['COD_DEPARTAMENTO'], how='left')
df_final = df_final.merge(df_grupos, on=['COD_DEPARTAMENTO'], how='left')
```

**Explicación de la estrategia de uniones:**
- Se usó una `inner join` entre la cobertura fija y móvil, ya que se necesitaba trabajar con municipios presentes en ambas bases.
- Se usó `left join` con revistas indexadas y grupos de investigación para no perder información de internet en municipios donde no hubiera registros en estas tablas.

---

## 4. Exportación de Datos Procesados

Una vez que los datos han sido limpiados y transformados, se exportan a un nuevo archivo CSV que servirá como insumo para análisis posteriores.

```python
df_final.to_csv("datos_procesados.csv", index=False)
```

---

## 5. Consideraciones Finales

### Desafíos Encontrados
- **Inconsistencia en nombres de municipios y departamentos**: Se resolvió mediante normalización y limpieza de strings.
- **Valores nulos en información geográfica**: Se usaron valores predeterminados y reglas de negocio para completarlos.
- **Registros duplicados en cobertura de internet móvil**: Se consolidaron mediante agregación.

### Futuras Mejoras
- Incorporación de datos de nuevas fuentes sobre producción científica.
- Refinamiento de la integración de datos de cobertura móvil para reflejar tendencias temporales.
- Desarrollo de modelos predictivos basados en estos datos para analizar el impacto de la conectividad en la investigación científica.

---

## 📜 Licencia
Este proyecto está licenciado bajo la licencia **Creative Commons** (CC BY 4.0). Puedes compartir y adaptar el contenido, siempre que se otorgue el crédito correspondiente. 

[![Licencia CC BY 4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

