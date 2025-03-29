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

📁 **[data](data/)**  
&nbsp;&nbsp;&nbsp;&nbsp;📂 **[processed](data/processed/)** – Datos finales y listos para modelado.  
&nbsp;&nbsp;&nbsp;&nbsp;📂 **[raw](data/raw/)** – Datos originales sin modificaciones.  

📁 **[extract](extract/)** – Archivos necesarios para la extracción de datos.  
📁 **[load](load/)** – Archivos para la carga de datos.  
📁 **[transform](transform/)** – Archivos para la transformación y limpieza de datos.  

📄 **[pipeline.py](pipeline.py)** – Script principal para la ejecución del pipeline ETL.  


## 📊 Identificación Inicial de Fuentes

| # | 📌 Fuente de Datos | 🌐 Origen | 📄 Tipo | 📦 Volumen |
|---|---------------|--------|------|---------|
| 1 | Cobertura móvil por tecnología, departamento y municipio | Datos Abiertos Colombia | CSV, API | ~41 MB |
| 2 | Internet fijo: Accesos por tecnología y segmento | Datos Abiertos Colombia | CSV, API | ~340 MB |
| 3 | Revistas Indexadas (Índice Nacional Publindex 2017-2020) | Datos Abiertos Colombia | CSV, XML | ~2 MB |
| 4 | Grupos de Investigación Reconocidos | Datos Abiertos Colombia | CSV, API | ~10 MB |

Estos datasets proporcionarán la base necesaria para realizar el análisis exploratorio, la transformación y la modelación de los datos. Al combinar la información sobre la cobertura de internet con los datos de producción científica, esperamos identificar correlaciones y patrones que puedan informar políticas públicas y estrategias de desarrollo.

## 📜 Licencia
Este proyecto está licenciado bajo la licencia **Creative Commons** (CC BY 4.0). Puedes compartir y adaptar el contenido, siempre que se otorgue el crédito correspondiente. 

[![Licencia CC BY 4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

