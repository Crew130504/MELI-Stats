# MELI Stats

Este proyecto es un **dashboard interactivo** construido con **Python + Streamlit + Snowflake** para explorar tendencias de productos en Mercado Libre, con foco en electrodomésticos (ventiladores, freidoras de aire, tipos de publicación, niveles de exposición, etc.).

La aplicación se conecta a **Snowflake**, donde se almacenan distintas tablas (`Q1`, `Q2`, `Q3567`, `Q4`, `Q8`) que representan subconjuntos de datos obtenidos a partir de la **API pública de Mercado Libre**, posteriormente procesados y cargados como CSV.

---

## Funcionalidades principales

El dashboard permite:

- Analizar **marcas más presentes** en ciertas categorías de productos.
- Visualizar el **top de modelos** de Air Fryer.
- Explorar la distribución de **niveles de exposición** y su peso relativo.
- Identificar **marcas predominantes** en un conjunto específico de electrodomésticos.
- Evaluar la relación entre **visibilidad y costo** de distintos tipos de publicación.
- Determinar qué tipo de publicación:
  - Requiere **mayor inversión** para lograr alta exposición.
  - Ofrece **mayor visibilidad general**.
- Ver el **top 3 de productos relacionados** con el electrodoméstico más vendido.

Todo se presenta mediante gráficas interactivas (barras, tortas, dispersión) y tablas con rankings resaltados.

---

## Arquitectura

- **Frontend / UI**: [Streamlit](https://streamlit.io/)  
- **Lógica y consultas**: Python  
- **Base de datos analítica**: [Snowflake](https://www.snowflake.com/)  
- **Visualización**: [Plotly Express](https://plotly.com/python/plotly-express/)  
- **Conexión a Snowflake**: `snowflake-connector-python`  
- **Gestión de credenciales**: variables de entorno cargadas con `python-dotenv`

---

## Estructura de datos (tablas en Snowflake)

Las tablas principales son:

- **`Q1`**  
  Universo base para analizar **marcas de ventiladores**.  
  Campos principales: `id`, `name`, `brand`.

- **`Q2`**  
  Lista ordenada de **modelos de Air Fryer** para construir un ranking.  
  Campo principal: `name`.

- **`Q3567`**  
  Datos agregados de distintos niveles/tipos de exposición (históricamente asociados a preguntas Q3, Q5, Q6 y Q7).  
  Campos principales:  
  - `name` (nivel/tipo de publicación)  
  - `highlight_score` (visibilidad)  
  - `sale_fee_amount` (costo/comisión)  
  - `valor_relativo` (peso relativo del nivel)

- **`Q4`**  
  Conjunto de productos para analizar **preferencia de marcas** en un subconjunto concreto de electrodomésticos.  
  Campos principales: `name`, `brand`.

- **`Q8`**  
  Ranking de productos relacionados con el electrodoméstico más vendido.  
  Campos principales: `ranking`, `name`, `brand`, `model`.

> ⚠️ Nota: La data fue obtenida a partir de la **API de Mercado Libre**, luego normalizada y cargada a Snowflake en forma de tablas analíticas.

---

## Requisitos

- **Python** 3.10+ (recomendado)
- Cuenta en **Snowflake** con:
  - Warehouse (por ejemplo `COMPUTE_WH`)
  - Base de datos y schema donde estén creadas las tablas `Q1`, `Q2`, `Q3567`, `Q4`, `Q8`.
- Paquetes Python:

```bash
pip install streamlit snowflake-connector-python pandas plotly python-dotenv
````

O, si hay `requirements.txt` en el repo:

```bash
pip install -r requirements.txt
```

---

## Configuración de variables de entorno

Este proyecto usa un archivo `.env` (no versionado en Git) para manejar credenciales y parámetros de conexión a Snowflake.

En la raíz del proyecto crea un archivo llamado **`.env`** con el siguiente contenido:

```env
SNOWFLAKE_ACCOUNT=tu_account_identifier      # ej: abcde-xy12345.us-east-1
SNOWFLAKE_USER=tu_usuario
SNOWFLAKE_PASSWORD=tu_contraseña
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=SNOWFLAKE_LEARNING_DB     # o la DB que estés usando
SNOWFLAKE_SCHEMA=PUBLIC                      # o el schema donde están Q1, Q2, Q3567, Q4, Q8
```

Asegúrate de que `.env` esté incluido en `.gitignore`.

---

## Ejecución local

1. Clonar el repositorio:

```bash
git clone https://github.com/<TU_USUARIO>/<TU_REPO>.git
cd <TU_REPO>
```

2. Crear y activar un entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

o

```bash
pip install streamlit snowflake-connector-python pandas plotly python-dotenv
```

4. Crear el archivo `.env` con los parámetros de Snowflake (ver sección anterior).

5. Ejecutar la aplicación:

```bash
streamlit run app.py
```

6. Abrir el navegador en la URL que indica Streamlit (normalmente `http://localhost:8501`).

---

## Notas sobre visualización

* La aplicación usa una **paleta de colores controlada**, donde el nivel o producto con mayor participación se representa en tonos de verde, seguido de amarillos/naranjas, rosas/morados y finalmente azules/turquesas, para mantener coherencia visual entre las gráficas.
* En algunos casos (por ejemplo, ranking de Air Fryers), se usan **tablas con filas resaltadas** (TOP 1, TOP 2, TOP 3) en lugar de gráficos circulares, para enfatizar el orden de importancia.

---

## Disclaimer

* Este proyecto utiliza datos obtenidos a través de la **API pública de Mercado Libre** con fines analíticos y de demostración técnica.
* “Mercado Libre” y los nombres de productos/marcas mostrados son propiedad de sus respectivos titulares.