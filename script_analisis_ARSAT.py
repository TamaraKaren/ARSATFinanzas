import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración General ---
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

print("--- Script de Análisis ARSAT Iniciado (Nivel Superior) ---")

#*****************************************************************************************************************
#********************************** FUNCIÓN PARA PROCESAR ÓRDENES DE COMPRA *************************************
#*****************************************************************************************************************
def procesar_y_analizar_ordenes_compra(ruta_archivo_oc):
    print("\n>>> [OC] Iniciando Procesamiento de Órdenes de Compra...")
    # ... (El contenido de esta función es el mismo que me pasaste, está bien) ...
    # --- Fase 1: Carga de Datos OC ---
    print(f"[OC] Intentando cargar el archivo de OC desde: {ruta_archivo_oc}")
    try:
        df = pd.read_csv(ruta_archivo_oc, encoding='latin1', delimiter=';')
        print("[OC] Archivo de OC cargado exitosamente!")
    except FileNotFoundError:
        print(f"[OC] Error: No se encontró el archivo de OC en la ruta especificada: {ruta_archivo_oc}")
        return None, None
    except Exception as e:
        print(f"[OC] Ocurrió un error al cargar el archivo de OC: {e}")
        return None, None

    print("\n[OC] DataFrame original de OC cargado:")
    df.info()
    print("-" * 50)

    # --- Fase 2: Limpieza y Preprocesamiento de Datos OC ---
    print("\n[OC] Iniciando Limpieza de Datos de OC...")
    df_limpio_oc = df.copy()
    
    columnas_totalmente_vacias = df_limpio_oc.columns[df_limpio_oc.isnull().all()].tolist()
    if columnas_totalmente_vacias:
        df_limpio_oc = df_limpio_oc.drop(columns=columnas_totalmente_vacias)
        print(f"[OC] Columnas OC completamente vacías {columnas_totalmente_vacias} eliminadas.")
    else:
        print("[OC] No se encontraron columnas OC completamente vacías para eliminar.")

    print("\n[OC] Nombres de columnas OC originales:", df_limpio_oc.columns.tolist())
    df_limpio_oc.columns = df_limpio_oc.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    print("[OC] Nombres de columnas OC limpiados:", df_limpio_oc.columns.tolist())

    columna_importe_oc = 'importe'
    columna_fecha_oc = 'fecha'
    columna_descripcion_producto_oc = 'descripcion_producto'

    if columna_importe_oc in df_limpio_oc.columns:
        print(f"[OC] Limpiando la columna OC '{columna_importe_oc}'...")
        df_limpio_oc[columna_importe_oc] = df_limpio_oc[columna_importe_oc].astype(str)
        df_limpio_oc[columna_importe_oc] = df_limpio_oc[columna_importe_oc].str.replace('$', '', regex=False).str.strip()
        df_limpio_oc[columna_importe_oc] = df_limpio_oc[columna_importe_oc].str.replace('.', '', regex=False)
        df_limpio_oc[columna_importe_oc] = df_limpio_oc[columna_importe_oc].str.replace(',', '.', regex=False)
        df_limpio_oc[columna_importe_oc] = pd.to_numeric(df_limpio_oc[columna_importe_oc], errors='coerce')
        print(f"[OC] Tipo de dato de '{columna_importe_oc}' ahora: {df_limpio_oc[columna_importe_oc].dtype}")

    if columna_descripcion_producto_oc in df_limpio_oc.columns and df_limpio_oc[columna_descripcion_producto_oc].isnull().any():
        df_limpio_oc[columna_descripcion_producto_oc] = df_limpio_oc[columna_descripcion_producto_oc].fillna('SIN DESCRIPCION')
        print(f"[OC] Valores faltantes en '{columna_descripcion_producto_oc}' rellenados.")

    columnas_categoricas_oc = ['moneda', 'gerencia', 'tipocompra']
    placeholder_faltante_oc = "No Especificado"
    for col_cat in columnas_categoricas_oc:
        if col_cat in df_limpio_oc.columns:
            df_limpio_oc[col_cat] = df_limpio_oc[col_cat].astype(str).str.strip().replace(['nan', ''], placeholder_faltante_oc)
    
    if columna_fecha_oc in df_limpio_oc.columns:
        print(f"[OC] Asegurando que la columna OC '{columna_fecha_oc}' es de tipo datetime...")
        df_limpio_oc[columna_fecha_oc] = pd.to_datetime(df_limpio_oc[columna_fecha_oc], dayfirst=True, errors='coerce')
        if df_limpio_oc[columna_fecha_oc].isnull().sum() == 0:
             print(f"[OC] Columna OC '{columna_fecha_oc}' convertida a datetime exitosamente.")
        else:
            print(f"[OC] ¡Atención! Algunos valores en la columna OC '{columna_fecha_oc}' no pudieron ser convertidos a fecha.")
    
    print("\n[OC] Fin de Limpieza de Datos de OC.")
    df_limpio_oc.info()

    # --- Fase 3: EDA para Órdenes de Compra ---
    print("\n\n[OC] Iniciando EDA para Órdenes de Compra...")
    if columna_importe_oc in df_limpio_oc.columns:
        plt.figure()
        sns.histplot(df_limpio_oc[columna_importe_oc], kde=True, bins=50)
        plt.title('Distribución de Importes (Órdenes de Compra)')
        plt.show() 
        print(f"\n[OC] Descripción estadística de '{columna_importe_oc}':")
        print(df_limpio_oc[columna_importe_oc].describe())
    
    if 'moneda' in df_limpio_oc.columns:
        plt.figure()
        sns.countplot(y=df_limpio_oc['moneda'], order = df_limpio_oc['moneda'].value_counts().index)
        plt.title('Conteo de Órdenes por Moneda (OC)')
        plt.show() 
    # (Aquí deberías tener el resto de tus gráficos de EDA para OC que estaban en versiones anteriores del script)
    # Por ejemplo: boxplot, top gerencias general y por moneda, etc. con sus plt.show()

    nombre_archivo_oc_formateado = 'ARSAT_Finanzas_ordenes_compra_FORMATEADO_FINAL.xlsx'
    try:
        df_para_excel_oc = df_limpio_oc.copy()
        nombres_encabezado_oc = [col.replace('_', ' ').title() for col in df_para_excel_oc.columns]
        if columna_fecha_oc in df_para_excel_oc.columns and pd.api.types.is_datetime64_any_dtype(df_para_excel_oc[columna_fecha_oc]):
             df_para_excel_oc[columna_fecha_oc] = df_para_excel_oc[columna_fecha_oc].dt.strftime('%d/%m/%Y')

        engine_kwargs_oc = {'options': {'strings_to_numbers': False, 'strings_to_formulas': False}}
        with pd.ExcelWriter(nombre_archivo_oc_formateado, engine='xlsxwriter', engine_kwargs=engine_kwargs_oc) as writer:
            df_para_excel_oc.to_excel(writer, sheet_name='Datos_Ordenes_Compra', index=False, header=False, startrow=1)
            workbook  = writer.book
            worksheet = writer.sheets['Datos_Ordenes_Compra']
            header_format = workbook.add_format({'bold': True, 'text_wrap': False, 'valign': 'vcenter', 'align': 'center', 'fg_color': '#D7E4BC', 'border': 1})
            for col_num, value in enumerate(nombres_encabezado_oc):
                worksheet.write(0, col_num, value, header_format)
            for i, col_original_name in enumerate(df_limpio_oc.columns):
                if col_original_name == columna_fecha_oc and df_para_excel_oc[columna_fecha_oc].notna().any() and isinstance(df_para_excel_oc[columna_fecha_oc].dropna().iloc[0], str) : # Check if not empty and first non-NaN is string
                    column_len = 12 
                else:
                    try: max_content_len = df_para_excel_oc[col_original_name].astype(str).map(len).max()
                    except: max_content_len = 10 
                    header_len = len(nombres_encabezado_oc[i])
                    column_len = max(max_content_len, header_len) + 2
                worksheet.set_column(i, i, min(column_len, 50))
            worksheet.freeze_panes(1, 0)
        print(f"\n[OC] DataFrame de OC limpio y formateado guardado como '{nombre_archivo_oc_formateado}'")
    except Exception as e:
        print(f"\n[OC] Error al guardar el archivo Excel de OC formateado: {e}")

    df_oc_pesos_mensual = None
    if columna_fecha_oc in df_limpio_oc.columns and df_limpio_oc[columna_fecha_oc].notnull().all():
        df_oc_pesos = df_limpio_oc[df_limpio_oc['moneda'] == 'Pesos'].copy()
        if not df_oc_pesos.empty and columna_importe_oc in df_oc_pesos.columns:
            df_oc_pesos_mensual = df_oc_pesos.set_index(columna_fecha_oc)[columna_importe_oc].resample('ME').sum()
            df_oc_pesos_mensual.name = 'gasto_ordenes_ars'
            
    print("<<< [OC] Fin Procesamiento de Órdenes de Compra.")
    return df_limpio_oc, df_oc_pesos_mensual


#*****************************************************************************************************************
#************************************ FUNCIÓN PARA PROCESAR TRANSFERENCIAS (CSV) - CORREGIDA ***********************
#*****************************************************************************************************************
def procesar_y_analizar_transferencias(ruta_archivo_transferencias_csv):
    print("\n\n>>> [TR] Iniciando Procesamiento de Transferencias...")
    print(f"[TR] Intentando cargar el archivo de transferencias CSV desde: {ruta_archivo_transferencias_csv}")
    try:
        # Leer el CSV asumiendo que la primera línea es el encabezado y la coma es el delimitador.
        # Pandas debería manejar las comillas alrededor de campos que contienen comas (como el importe).
        df_transferencias = pd.read_csv(ruta_archivo_transferencias_csv, encoding='latin1', dtype=str)
        
        print("[TR] Archivo de transferencias CSV cargado.")
        print("[TR] Nombres de columna originales de transferencias:", df_transferencias.columns.tolist())

        # Limpiar nombres de columna (minúsculas, guion bajo)
        df_transferencias.columns = [col.strip().lower().replace(' ', '_') for col in df_transferencias.columns]
        nombres_columnas_transf = df_transferencias.columns.tolist()
        print(f"[TR] Nombres de columna transferencias limpiados: {nombres_columnas_transf}")

        # Verificar si tenemos las 3 columnas esperadas
        if len(nombres_columnas_transf) != 3: # Esperamos exactamente 3 columnas
            print(f"[TR] Error: Se esperaban 3 columnas, pero se encontraron {len(nombres_columnas_transf)}.")
            print(f"[TR] Columnas encontradas: {nombres_columnas_transf}")
            print("[TR] Primeras filas del df leído:")
            print(df_transferencias.head())
            return None, None # Retornar None si la estructura no es la esperada

    except FileNotFoundError:
        print(f"[TR] Error: No se encontró el archivo de transferencias CSV: {ruta_archivo_transferencias_csv}")
        return None, None
    except Exception as e:
        print(f"[TR] Ocurrió un error al cargar el archivo de transferencias CSV: {e}")
        return None, None

    # Asignar nombres de columna clave de forma más robusta, asumiendo el orden si los nombres son genéricos
    # o usando los nombres limpiados si son descriptivos.
    # Si los nombres limpiados son 'desembolsos', 'fecha', 'importe', se usarán esos.
    # Si son genéricos como '0', '1', '2', los reasignamos.
    if nombres_columnas_transf == ['0', '1', '2']: # Caso de nombres genéricos si read_csv no tomó encabezado
        df_transferencias.columns = ['desembolso', 'fecha', 'importe']
        nombres_columnas_transf = df_transferencias.columns.tolist()

    col_desc_transf = nombres_columnas_transf[0] # Asumimos que la primera es descripción
    col_fecha_transf = nombres_columnas_transf[1] # Asumimos que la segunda es fecha
    col_importe_transf = nombres_columnas_transf[2] # Asumimos que la tercera es importe
    
    # Limpieza de Tipos de Datos
    if col_importe_transf in df_transferencias.columns:
        print(f"[TR] Limpiando la columna transferencias '{col_importe_transf}'...")
        df_transferencias[col_importe_transf] = df_transferencias[col_importe_transf].astype(str)
        df_transferencias[col_importe_transf] = df_transferencias[col_importe_transf].str.replace('"', '', regex=False)
        df_transferencias[col_importe_transf] = df_transferencias[col_importe_transf].str.replace('$', '', regex=False).str.strip()
        df_transferencias[col_importe_transf] = df_transferencias[col_importe_transf].str.replace('.', '', regex=False)
        df_transferencias[col_importe_transf] = df_transferencias[col_importe_transf].str.replace(',', '.', regex=False)
        df_transferencias[col_importe_transf] = pd.to_numeric(df_transferencias[col_importe_transf], errors='coerce')
        print(f"[TR] Tipo de dato de '{col_importe_transf}' ahora: {df_transferencias[col_importe_transf].dtype}")

    if col_fecha_transf in df_transferencias.columns:
        print(f"[TR] Limpiando y convirtiendo la columna transferencias '{col_fecha_transf}'...")
        df_transferencias[col_fecha_transf] = df_transferencias[col_fecha_transf].str.strip()
        df_transferencias[col_fecha_transf] = pd.to_datetime(df_transferencias[col_fecha_transf], dayfirst=True, errors='coerce')
        print(f"[TR] Tipo de dato de '{col_fecha_transf}' ahora: {df_transferencias[col_fecha_transf].dtype}")

    if col_desc_transf in df_transferencias.columns:
        df_transferencias[col_desc_transf] = df_transferencias[col_desc_transf].str.strip()
    
    print("\n[TR] DataFrame de Transferencias Limpio:")
    df_transferencias.info()
    print(df_transferencias.head())

    print("\n\n[TR] Iniciando EDA para Transferencias...")
    if col_importe_transf in df_transferencias.columns and pd.api.types.is_numeric_dtype(df_transferencias[col_importe_transf]):
        plt.figure()
        sns.histplot(df_transferencias[col_importe_transf], kde=True, bins=min(10, len(df_transferencias)))
        plt.title('Distribución de Importes de Transferencias')
        plt.show() 
    
    df_transf_mensual = None
    if col_fecha_transf in df_transferencias.columns and \
       df_transferencias[col_fecha_transf].notnull().all() and \
       col_importe_transf in df_transferencias.columns and \
       pd.api.types.is_numeric_dtype(df_transferencias[col_importe_transf]):
        
        df_transf_temporal = df_transferencias.set_index(col_fecha_transf)
        df_transf_mensual = df_transf_temporal[col_importe_transf].resample('ME').sum()
        df_transf_mensual.name = 'ingreso_transferencias'
        print("\n[TR] Importe Total de Transferencias por Mes:")
        print(df_transf_mensual.head())
        plt.figure(figsize=(15,7))
        df_transf_mensual.plot(kind='line', marker='o')
        plt.title('Importe Total de Transferencias por Mes')
        plt.show() 
        
    nombre_archivo_transf_formateado = 'ARSAT_Finanzas_transferencias_FORMATEADO.xlsx'
    try:
        df_para_excel_transf = df_transferencias.copy()
        nombres_encabezado_transf = [col.replace('_', ' ').title() for col in df_para_excel_transf.columns]
        if col_fecha_transf in df_para_excel_transf.columns and pd.api.types.is_datetime64_any_dtype(df_para_excel_transf[col_fecha_transf]):
             df_para_excel_transf[col_fecha_transf] = df_para_excel_transf[col_fecha_transf].dt.strftime('%d/%m/%Y')
        
        engine_kwargs_transf = {'options': {'strings_to_numbers': False, 'strings_to_formulas': False}}
        with pd.ExcelWriter(nombre_archivo_transf_formateado, engine='xlsxwriter', engine_kwargs=engine_kwargs_transf) as writer:
            df_para_excel_transf.to_excel(writer, sheet_name='Datos_Transferencias', index=False, header=False, startrow=1)
            workbook  = writer.book
            worksheet = writer.sheets['Datos_Transferencias']
            header_format = workbook.add_format({'bold': True, 'text_wrap': False, 'valign': 'vcenter', 'align': 'center', 'fg_color': '#C9DAF8', 'border': 1})
            for col_num, value in enumerate(nombres_encabezado_transf):
                worksheet.write(0, col_num, value, header_format)
            for i, col_original_name in enumerate(df_transferencias.columns):
                if col_original_name == col_fecha_transf and df_para_excel_transf[col_fecha_transf].notna().any() and isinstance(df_para_excel_transf[col_fecha_transf].dropna().iloc[0], str) :
                    column_len = 12 
                else:
                    try: max_content_len = df_para_excel_transf[col_original_name].astype(str).map(len).max()
                    except: max_content_len = 10 
                    header_len = len(nombres_encabezado_transf[i])
                    column_len = max(max_content_len, header_len) + 2
                worksheet.set_column(i, i, min(column_len, 50))
            worksheet.freeze_panes(1, 0)
        print(f"\n[TR] DataFrame de Transferencias limpio y formateado guardado como '{nombre_archivo_transf_formateado}'")
    except Exception as e:
        print(f"\n[TR] Error al guardar el archivo Excel de Transferencias formateado: {e}")
        
    print("<<< [TR] Fin Procesamiento de Transferencias.")
    return df_transferencias, df_transf_mensual


#*****************************************************************************************************************
#******************************************** SCRIPT PRINCIPAL **************************************************
#*****************************************************************************************************************
print("\n--- SCRIPT PRINCIPAL: INICIO DE EJECUCIÓN ---")

# --- Procesar Órdenes de Compra ---
ruta_ordenes_compra = r"C:\Tamara\Programación\Proyectos\Limpieza de datos datasets\ARSAT Finanzas\ARSAT_Finanzas_ordenes_de_compra-2022_marzo_2023.csv"
print(f"\n--- Llamando a procesar_y_analizar_ordenes_compra con ruta: {ruta_ordenes_compra} ---")
df_oc_limpio, df_oc_pesos_mensual = procesar_y_analizar_ordenes_compra(ruta_ordenes_compra)
print("--- Retorno de procesar_y_analizar_ordenes_compra recibido ---")

# --- Procesar Transferencias ---
ruta_transferencias_recibidas_csv = r'C:\Tamara\Programación\Proyectos\Limpieza de datos datasets\ARSAT Finanzas\transferencias-recibidas-2020-v5.csv'
print(f"\n--- Llamando a procesar_y_analizar_transferencias con ruta: {ruta_transferencias_recibidas_csv} ---")
df_transf_limpio, df_transf_mensual = procesar_y_analizar_transferencias(ruta_transferencias_recibidas_csv)
print("--- Retorno de procesar_y_analizar_transferencias recibido ---")


# --- Fase de Correlación (si ambos DataFrames mensuales están disponibles) ---
print("\n\n--- Iniciando Fase de Correlación ---")
if df_oc_pesos_mensual is not None and df_transf_mensual is not None:
    print("[CORR] DataFrames mensuales disponibles para correlación.")
    df_correlacion = pd.merge(df_transf_mensual, df_oc_pesos_mensual, 
                              left_index=True, right_index=True, how='inner')
    
    print("\n[CORR] Datos mensuales para correlación (Transferencias vs Órdenes en ARS):")
    print(df_correlacion.head())

    if len(df_correlacion) > 1:
        correlacion_calculada = df_correlacion['ingreso_transferencias'].corr(df_correlacion['gasto_ordenes_ars'])
        print(f"\n[CORR] Correlación entre ingresos por transferencias y gastos de órdenes (ARS) mensuales: {correlacion_calculada:.2f}")

        plt.figure(figsize=(8, 8))
        sns.scatterplot(data=df_correlacion, x='ingreso_transferencias', y='gasto_ordenes_ars')
        sns.regplot(data=df_correlacion, x='ingreso_transferencias', y='gasto_ordenes_ars', scatter=False, color='red')
        plt.title('Correlación: Transferencias Recibidas vs. Gasto Órdenes (ARS) Mensual')
        plt.xlabel('Total Transferencias Recibidas por Mes')
        plt.ylabel('Total Gasto Órdenes (ARS) por Mes')
        plt.ticklabel_format(style='plain', axis='both')
        plt.grid(True)
        plt.show() 
    else:
        print("\n[CORR] No hay suficientes datos mensuales superpuestos para calcular o visualizar la correlación.")
else:
    print("\n[CORR] No se pueden realizar los cálculos de correlación debido a que faltan datos mensuales de órdenes o transferencias.")

print("\n\n--- ANÁLISIS COMPLETO FINALIZADO ---")