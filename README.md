# Análisis Financiero ARSAT y Dashboard Interactivo

Este proyecto realiza un análisis de datos financieros de ARSAT, enfocándose en órdenes de compra y transferencias recibidas. Incluye limpieza de datos, análisis exploratorio (EDA) con visualizaciones, y presenta los resultados en un dashboard interactivo creado con Streamlit. Adicionalmente, se proporciona una utilidad para empaquetar el dashboard como una aplicación ejecutable.

## 🚀 Dashboard Interactivo en Vivo

¡Explora los datos y análisis de forma interactiva!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tamaramonzon-arsatfinanzas-app.streamlit.app/)

**Enlace directo:** [https://tamaramonzon-arsatfinanzas-app.streamlit.app/](https://tamaramonzon-arsatfinanzas-app.streamlit.app/)

## Características Principales

*   **Procesamiento de Datos de Órdenes de Compra:**
    *   Carga de datos desde un archivo CSV.
    *   Limpieza exhaustiva: manejo de tipos de datos, valores faltantes, nombres de columnas.
    *   Análisis exploratorio detallado: distribución de importes, análisis por moneda, gerencia, proveedor, tipo de compra y tendencias temporales.
    *   Generación de un archivo Excel (`.xlsx`) formateado con los datos limpios.
*   **Procesamiento de Datos de Transferencias Recibidas:**
    *   Carga de datos desde un archivo CSV con formato no estándar.
    *   Estructuración y limpieza de los datos.
    *   Análisis exploratorio básico: distribución de importes y análisis temporal.
    *   Generación de un archivo Excel (`.xlsx`) formateado con los datos limpios.
*   **Análisis de Correlación (Conceptual):**
    *   Intento de correlacionar ingresos por transferencias con gastos de órdenes de compra (limitado por el solapamiento temporal de los datasets de ejemplo).
*   **Dashboard Interactivo con Streamlit:**
    *   Visualización de los análisis de Órdenes de Compra y Transferencias.
    *   Filtros interactivos por rango de fechas y moneda.
    *   Presentación organizada en pestañas.
*   **Empaquetado como Aplicación Ejecutable (Opcional):**
    *   Incluye un script lanzador (`run_dashboard.py`) y las instrucciones para usar PyInstaller para crear un archivo `.exe` para facilitar la ejecución sin un entorno Python.

## Estructura del Proyecto

*   `dashboard_arsat.py`: Script principal de Python que contiene la lógica de la aplicación Streamlit y las funciones de procesamiento de datos.
*   `run_dashboard.py`: (Opcional) Script lanzador para ayudar a empaquetar la aplicación Streamlit con PyInstaller.
*   `ARSAT_Finanzas_ordenes_de_compra-2022_marzo_2023.csv`: Archivo de datos de ejemplo para órdenes de compra.
*   `transferencias-recibidas-2020-v5.csv`: Archivo de datos de ejemplo para transferencias recibidas.
*   `requirements.txt`: Lista de dependencias de Python necesarias.
*   `README.md`: Este archivo.
*   `img/`: (Sugerencia) Carpeta para guardar capturas de pantalla del dashboard para el README.

## Requisitos Previos

*   Python 3.9 o superior.
*   `pip` (gestor de paquetes de Python).

## Instalación

1.  **Clona el repositorio (o descarga los archivos):**
    ```bash
    git clone https://github.com/TamaraKaren/ARSATFinanzas.git
    cd ARSATFinanzas
    ```

2.  **(Recomendado) Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    Si también planeas crear el ejecutable, instala PyInstaller:
    ```bash
    pip install pyinstaller
    ```

## Uso

### Ejecutar el Dashboard de Streamlit

1.  Asegúrate de que los archivos CSV de datos (`ARSAT_Finanzas_ordenes_de_compra-2022_marzo_2023.csv` y `transferencias-recibidas-2020-v5.csv`) estén en la misma carpeta que `dashboard_arsat.py`.
2.  Abre una terminal en la carpeta raíz del proyecto.
3.  Ejecuta el siguiente comando:
    ```bash
    streamlit run dashboard_arsat.py
    ```
4.  El dashboard se abrirá automáticamente en tu navegador web predeterminado (usualmente en `http://localhost:8501`).

### (Opcional) Crear un Ejecutable (.exe)

Si deseas crear un archivo `.exe` para ejecutar el dashboard sin necesidad de un entorno Python configurado:

1.  Asegúrate de tener PyInstaller instalado (`pip install pyinstaller`).
2.  Asegúrate de que los archivos `dashboard_arsat.py`, `run_dashboard.py`, y los dos archivos CSV de datos estén en la misma carpeta.
3.  Abre una terminal en la carpeta raíz del proyecto.
4.  Ejecuta el siguiente comando de PyInstaller:
    ```bash
    pyinstaller --name "DashboardAnalisisARSAT" ^
    --add-data "dashboard_arsat.py:." ^
    --add-data "ARSAT_Finanzas_ordenes_de_compra-2022_marzo_2023.csv:." ^
    --add-data "transferencias-recibidas-2020-v5.csv:." ^
    run_dashboard.py
    ```
    *   *Nota para PowerShell:* Reemplaza el carácter de continuación de línea `^` por `` ` ``.
    *   Para una mejor experiencia de usuario final (un solo archivo, sin consola para el lanzador), puedes probar:
        ```bash
        pyinstaller --name "DashboardAnalisisARSAT" --onefile --windowed ^
        --add-data "dashboard_arsat.py:." ^
        --add-data "ARSAT_Finanzas_ordenes_de_compra-2022_marzo_2023.csv:." ^
        --add-data "transferencias-recibidas-2020-v5.csv:." ^
        run_dashboard.py
        ```

5.  PyInstaller creará una carpeta `dist`. Dentro de ella, encontrarás una subcarpeta `DashboardAnalisisARSAT` (o solo el archivo `DashboardAnalisisARSAT.exe` si usaste `--onefile`).
6.  Copia toda la carpeta `DashboardAnalisisARSAT` (o el `.exe` único) a la ubicación deseada y ejecuta el archivo `.exe`.

## Detalles del Análisis

*(Aquí puedes añadir un breve resumen de los principales hallazgos o los tipos de análisis que realiza el dashboard, por ejemplo:)*

*   Análisis de gastos por gerencia, proveedor y tipo de compra, segmentado por moneda.
*   Visualización de tendencias de gastos e ingresos a lo largo del tiempo.
*   Identificación de las transacciones de mayor valor.
*   Exploración de la correlación entre ingresos y gastos (condicionada a la disponibilidad de datos solapados).

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un "issue" para discutir cambios importantes o reportar errores.

## Autor

*   Tamara Monzón Fontano


Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
