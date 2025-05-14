import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
from datetime import date 
import os 
import sys 

# --- Función para obtener la ruta correcta de los archivos (para PyInstaller) ---
def get_path(filename):
    if hasattr(sys, "_MEIPASS"): 
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

# --- Configuración General de Streamlit y Gráficos ---
st.set_page_config(layout="wide", page_title="Análisis Financiero ARSAT")
sns.set_style("whitegrid") 

# --- Función Auxiliar de Formato ---
def format_value_with_si_dot_sep(value, prefix=""):
    if pd.isna(value) or not isinstance(value, (int, float)): return ""
    abs_value = abs(value)
    if abs_value >= 1_000_000_000: val_str = f"{value / 1_000_000_000:,.1f}G"
    elif abs_value >= 1_000_000: val_str = f"{value / 1_000_000:,.1f}M"
    elif abs_value >= 1_000: val_str = f"{value / 1_000:,.1f}K"
    else: val_str = f"{value:,.0f}"
    formatted_str = val_str.replace(",", "X").replace(".", ",").replace("X", ".")
    return prefix + formatted_str

def format_tick_value(value, prefix=""):
    if pd.isna(value): return ""
    return f"{prefix}{value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Funciones de Carga y Procesamiento de Datos (Cacheadas) ---
@st.cache_data 
def cargar_y_procesar_ordenes_compra_st(ruta_archivo_oc):
    # ... (Contenido COMPLETO de esta función como en la última versión que funcionó)
    print("\n>>> [OC ST] Iniciando Procesamiento de Órdenes de Compra para Streamlit...")
    try:
        df = pd.read_csv(ruta_archivo_oc, encoding='latin1', delimiter=';')
    except Exception as e:
        st.error(f"[OC] Error al cargar archivo de OC: {e}")
        return None, None, None 
    
    df_limpio_oc = df.copy()
    df_limpio_oc.columns = df_limpio_oc.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    
    columna_importe_oc = 'importe'
    columna_fecha_oc = 'fecha'
    
    if columna_importe_oc in df_limpio_oc.columns:
        df_limpio_oc[columna_importe_oc] = df_limpio_oc[columna_importe_oc].astype(str).str.replace('$', '', regex=False).str.strip().str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df_limpio_oc[columna_importe_oc] = pd.to_numeric(df_limpio_oc[columna_importe_oc], errors='coerce')

    if 'descripcion_producto' in df_limpio_oc.columns and df_limpio_oc['descripcion_producto'].isnull().any():
        df_limpio_oc['descripcion_producto'] = df_limpio_oc['descripcion_producto'].fillna('SIN DESCRIPCION')

    columnas_categoricas_oc = ['moneda', 'gerencia', 'tipocompra']
    placeholder_faltante_oc = "No Especificado"
    for col_cat in columnas_categoricas_oc:
        if col_cat in df_limpio_oc.columns:
            df_limpio_oc[col_cat] = df_limpio_oc[col_cat].astype(str).str.strip().replace(['nan', ''], placeholder_faltante_oc)
    
    if columna_fecha_oc in df_limpio_oc.columns:
        df_limpio_oc[columna_fecha_oc] = pd.to_datetime(df_limpio_oc[columna_fecha_oc], dayfirst=True, errors='coerce')
    
    df_oc_pesos_mensual = None
    df_oc_dolares_mensual = None
    
    if columna_fecha_oc in df_limpio_oc.columns and df_limpio_oc[columna_fecha_oc].notnull().all():
        df_oc_pesos = df_limpio_oc[df_limpio_oc['moneda'] == 'Pesos'].copy()
        if not df_oc_pesos.empty and columna_importe_oc in df_oc_pesos.columns:
            df_oc_pesos_mensual = df_oc_pesos.set_index(columna_fecha_oc)[columna_importe_oc].resample('ME').sum()
            df_oc_pesos_mensual.name = 'gasto_ordenes_ars'
        df_oc_dolares = df_limpio_oc[df_limpio_oc['moneda'] == 'Dólares'].copy()
        if not df_oc_dolares.empty and columna_importe_oc in df_oc_dolares.columns:
            df_oc_dolares_mensual = df_oc_dolares.set_index(columna_fecha_oc)[columna_importe_oc].resample('ME').sum()
            df_oc_dolares_mensual.name = 'gasto_ordenes_usd'
            
    print("<<< [OC ST] Fin Procesamiento de Órdenes de Compra para Streamlit.")
    return df_limpio_oc, df_oc_pesos_mensual, df_oc_dolares_mensual

@st.cache_data
def cargar_y_procesar_transferencias_st(ruta_archivo_transferencias_csv):
    # ... (Contenido COMPLETO de esta función como en la última versión que funcionó)
    print("\n\n>>> [TR ST] Iniciando Procesamiento de Transferencias para Streamlit...")
    try:
        df_transferencias = pd.read_csv(ruta_archivo_transferencias_csv, encoding='latin1', dtype=str)
    except Exception as e:
        st.error(f"[TR] Error al cargar archivo de transferencias: {e}")
        return None, None

    df_transferencias.columns = [col.strip().lower().replace(' ', '_') for col in df_transferencias.columns]
    if len(df_transferencias.columns) != 3:
        st.error(f"[TR] Error: Se esperaban 3 columnas en transferencias, se encontraron {len(df_transferencias.columns)}.")
        return None, None

    df_transferencias.columns = ['desembolso', 'fecha', 'importe'] 

    col_desc_transf = 'desembolso'
    col_fecha_transf = 'fecha'
    col_importe_transf = 'importe'
    
    if col_importe_transf in df_transferencias.columns:
        df_transferencias[col_importe_transf] = df_transferencias[col_importe_transf].astype(str).str.replace('"', '', regex=False).str.replace('$', '', regex=False).str.strip().str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df_transferencias[col_importe_transf] = pd.to_numeric(df_transferencias[col_importe_transf], errors='coerce')

    if col_fecha_transf in df_transferencias.columns:
        df_transferencias[col_fecha_transf] = pd.to_datetime(df_transferencias[col_fecha_transf], dayfirst=True, errors='coerce')

    if col_desc_transf in df_transferencias.columns:
        df_transferencias[col_desc_transf] = df_transferencias[col_desc_transf].str.strip()
    
    df_transf_mensual = None
    if col_fecha_transf in df_transferencias.columns and \
       df_transferencias[col_fecha_transf].notnull().all() and \
       col_importe_transf in df_transferencias.columns and \
       pd.api.types.is_numeric_dtype(df_transferencias[col_importe_transf]):
        df_transf_temporal = df_transferencias.set_index(col_fecha_transf)
        df_transf_mensual = df_transf_temporal[col_importe_transf].resample('ME').sum()
        df_transf_mensual.name = 'ingreso_transferencias'
        
    print("<<< [TR ST] Fin Procesamiento de Transferencias para Streamlit.")
    return df_transferencias, df_transf_mensual

# --- Carga de Datos ---
ruta_oc_main = get_path("ARSAT_Finanzas_ordenes_de_compra-2022_marzo_2023.csv")
ruta_tr_main = get_path('transferencias-recibidas-2020-v5.csv')

df_oc, df_oc_mensual_ars, df_oc_mensual_usd = cargar_y_procesar_ordenes_compra_st(ruta_oc_main)
df_tr, df_tr_mensual = cargar_y_procesar_transferencias_st(ruta_tr_main)

# --- Título del Dashboard ---
st.title("📊 Dashboard de Análisis Financiero ARSAT")

# --- Barra Lateral para Filtros ---
st.sidebar.header("Filtros y Opciones")

df_oc_filtrado_fecha = df_oc.copy() if df_oc is not None else pd.DataFrame() 
if df_oc is not None and 'fecha' in df_oc.columns and not df_oc.empty:
    min_fecha_oc_val = df_oc['fecha'].min()
    max_fecha_oc_val = df_oc['fecha'].max()
    if pd.NaT not in [min_fecha_oc_val, max_fecha_oc_val] and min_fecha_oc_val <= max_fecha_oc_val:
        date_selection_oc = st.sidebar.date_input(
            "Rango o Fecha Única (Órdenes de Compra):",
            value=(min_fecha_oc_val.date(), max_fecha_oc_val.date()), 
            min_value=min_fecha_oc_val.date(),
            max_value=max_fecha_oc_val.date(),
            key="oc_date_selector" 
        )
        if isinstance(date_selection_oc, (tuple, list)) and len(date_selection_oc) == 2:
            fecha_inicio_oc, fecha_fin_oc = date_selection_oc
            df_oc_filtrado_fecha = df_oc[
                (df_oc['fecha'] >= pd.to_datetime(fecha_inicio_oc)) & 
                (df_oc['fecha'] <= pd.to_datetime(fecha_fin_oc))
            ]
        elif isinstance(date_selection_oc, date): 
            fecha_unica_oc = pd.to_datetime(date_selection_oc)
            df_oc_filtrado_fecha = df_oc[df_oc['fecha'].dt.normalize() == fecha_unica_oc.normalize()]
    else:
        st.sidebar.warning("Fechas base inválidas para filtro de OC.")
elif df_oc is None:
    st.sidebar.error("Datos de Órdenes de Compra no disponibles.")

moneda_oc_sel = None
df_oc_final_filtrado = pd.DataFrame() 
if df_oc_filtrado_fecha is not None and not df_oc_filtrado_fecha.empty:
    monedas_oc_disponibles = sorted(df_oc_filtrado_fecha['moneda'].unique())
    if monedas_oc_disponibles:
        moneda_oc_sel = st.sidebar.selectbox("Moneda (Órdenes de Compra):", monedas_oc_disponibles, key="oc_moneda_sel")
        if moneda_oc_sel: 
             df_oc_final_filtrado = df_oc_filtrado_fecha[df_oc_filtrado_fecha['moneda'] == moneda_oc_sel]
    else:
        st.sidebar.text("No hay monedas para el filtro actual de OC.")
else:
    st.sidebar.text("No hay datos de OC para filtrar por moneda.")


# --- Sección Principal con Pestañas ---
tab_oc, tab_transferencias = st.tabs(["Órdenes de Compra", "Transferencias Recibidas"]) # CORREGIDO: Eliminada pestaña Correlación

with tab_oc:
    st.header("Análisis de Órdenes de Compra")
    if not df_oc_final_filtrado.empty:
        st.metric("Nº Órdenes (Filtros Aplicados)", len(df_oc_final_filtrado))
        fecha_min_display = df_oc_final_filtrado['fecha'].min().strftime('%d/%m/%Y') if pd.notna(df_oc_final_filtrado['fecha'].min()) else 'N/A'
        fecha_max_display = df_oc_final_filtrado['fecha'].max().strftime('%d/%m/%Y') if pd.notna(df_oc_final_filtrado['fecha'].max()) else 'N/A'
        st.subheader(f"Visualizaciones para {moneda_oc_sel} (Rango: {fecha_min_display} - {fecha_max_display})")
        
        moneda_simbolo_oc = ""
        if moneda_oc_sel == "Pesos": moneda_simbolo_oc = "ARS$ "
        elif moneda_oc_sel == "Dólares": moneda_simbolo_oc = "U$D "
        elif moneda_oc_sel == "Euro": moneda_simbolo_oc = "€ "

        col1_oc_dist, col2_oc_dist = st.columns(2)
        with col1_oc_dist:
            st.write("Distribución de Importes:")
            fig_hist_oc = px.histogram(df_oc_final_filtrado, x='importe', marginal="box", title=f"Distribución de Importes ({moneda_oc_sel})", color_discrete_sequence=['#636EFA'])
            fig_hist_oc.update_layout(bargap=0.1, xaxis_title="Importe", yaxis_title="Frecuencia", xaxis_tickformat='.,.0f', height=450) 
            st.plotly_chart(fig_hist_oc, use_container_width=True)
        
        with col2_oc_dist:
            st.write("Conteo por Tipo de Compra:")
            conteo_tipocompra = df_oc_final_filtrado['tipocompra'].value_counts().reset_index()
            conteo_tipocompra.columns = ['tipocompra', 'cantidad']
            top_n_tipocompra = conteo_tipocompra.head(10).sort_values(by='cantidad', ascending=False) 
            fig_tipo_compra = px.bar(top_n_tipocompra, y='tipocompra', x='cantidad', orientation='h', title=f"Top 10 Tipos de Compra ({moneda_oc_sel})", text='cantidad') 
            fig_tipo_compra.update_traces(textposition='outside', textfont_size=10)
            fig_tipo_compra.update_layout(yaxis_title="Tipo de Compra", xaxis_title="Cantidad de Órdenes", height=450, showlegend=False, yaxis={'categoryorder':'total ascending'}, margin=dict(l=180, r=20, t=50, b=70))
            st.plotly_chart(fig_tipo_compra, use_container_width=True)

        st.subheader(f"Análisis por Gerencia y Proveedor ({moneda_oc_sel})")
        
        st.write("Top 5 Gerencias por Gasto:")
        top_gerencias_oc = df_oc_final_filtrado.groupby('gerencia')['importe'].sum().nlargest(5).reset_index().sort_values(by='importe', ascending=False)
        top_gerencias_oc['importe_display'] = top_gerencias_oc['importe'].apply(lambda x: format_value_with_si_dot_sep(x, ""))

        fig_gerencias = px.bar(top_gerencias_oc, y='gerencia', x='importe', title=f"Top 5 Gerencias ({moneda_oc_sel})", orientation='h', text='importe_display')
        fig_gerencias.update_traces(textposition='auto', textfont_size=9) 
        fig_gerencias.update_layout(
            xaxis_title="Importe Total", 
            yaxis_title="Gerencia", 
            xaxis_tickprefix=moneda_simbolo_oc, 
            xaxis_tickformat='~s', 
            height=400, 
            showlegend=False,
            yaxis={'categoryorder':'total ascending', 'tickfont': {'size': 10}, 'automargin': False}, 
            xaxis={'automargin': True, 'title_font': {'size': 12}, 'tickangle': 0, 'nticks': 5}, 
            margin=dict(l=350, r=10, t=50, b=80) 
        )
        st.plotly_chart(fig_gerencias, use_container_width=True)

        st.write("Top 5 Proveedores por Gasto:")
        top_proveedores_oc = df_oc_final_filtrado.groupby('proveedor')['importe'].sum().nlargest(5).reset_index().sort_values(by='importe', ascending=False)
        top_proveedores_oc['importe_display'] = top_proveedores_oc['importe'].apply(lambda x: format_value_with_si_dot_sep(x, ""))

        fig_proveedores = px.bar(top_proveedores_oc, y='proveedor', x='importe', title=f"Top 5 Proveedores ({moneda_oc_sel})", orientation='h', text='importe_display')
        fig_proveedores.update_traces(textposition='auto', textfont_size=9) 
        fig_proveedores.update_layout(
            xaxis_title="Importe Total", 
            yaxis_title="Proveedor", 
            xaxis_tickprefix=moneda_simbolo_oc, 
            xaxis_tickformat='~s', 
            height=400, 
            showlegend=False, 
            yaxis={'categoryorder':'total ascending', 'tickfont': {'size': 10}, 'automargin': False}, 
            xaxis={'automargin': True, 'title_font': {'size': 12}, 'tickangle': 0, 'nticks': 5}, 
            margin=dict(l=350, r=10, t=50, b=80) 
        )
        st.plotly_chart(fig_proveedores, use_container_width=True)

        if 'fecha' in df_oc_final_filtrado.columns and not df_oc_final_filtrado.empty:
            gasto_mensual_filtrado_oc = df_oc_final_filtrado.set_index('fecha')['importe'].resample('ME').sum().reset_index() 
            if not gasto_mensual_filtrado_oc.empty:
                st.subheader(f"Gasto Mensual ({moneda_oc_sel})")
                gasto_mensual_grafico_oc = gasto_mensual_filtrado_oc.rename(columns={'fecha': 'Fecha'})
                fig_gasto_mensual_oc = px.line(gasto_mensual_grafico_oc, x='Fecha', y='importe', markers=True, title=f"Gasto Mensual ({moneda_oc_sel})")
                
                y_values_oc = gasto_mensual_grafico_oc['importe']
                if not y_values_oc.empty and pd.notna(y_values_oc.max()) and y_values_oc.max() > 0:
                    num_ticks_y = 5
                    max_y_val = y_values_oc.max() 
                    min_y_val = 0 
                    tickvals_oc = np.linspace(min_y_val, max_y_val, num_ticks_y)
                    tickvals_oc = [v for v in tickvals_oc if pd.notna(v)] 
                    if not tickvals_oc: tickvals_oc = [0] 
                    ticktext_oc = [format_tick_value(val, moneda_simbolo_oc) for val in tickvals_oc]
                    fig_gasto_mensual_oc.update_layout(yaxis_title=f"Importe Total", xaxis_title="Fecha", yaxis_tickvals=tickvals_oc, yaxis_ticktext=ticktext_oc)
                else:
                    fig_gasto_mensual_oc.update_layout(yaxis_title=f"Importe Total", xaxis_title="Fecha", yaxis_tickprefix=moneda_simbolo_oc, yaxis_tickformat='~s')
                st.plotly_chart(fig_gasto_mensual_oc, use_container_width=True)
        
        st.subheader(f"Detalle de Órdenes de Mayor Valor ({moneda_oc_sel})")
        num_outliers_oc = st.slider("Número de órdenes a mostrar:", 1, 20, 5, key="oc_outliers_slider")
        top_n_ordenes_oc = df_oc_final_filtrado.nlargest(num_outliers_oc, 'importe')
        
        df_outliers_display = top_n_ordenes_oc.copy()
        if 'fecha' in df_outliers_display.columns:
            if pd.api.types.is_datetime64_any_dtype(df_outliers_display['fecha']):
                df_outliers_display['Fecha Formateada'] = df_outliers_display['fecha'].dt.strftime('%d/%m/%Y')
            else:
                try: df_outliers_display['Fecha Formateada'] = pd.to_datetime(df_outliers_display['fecha']).dt.strftime('%d/%m/%Y')
                except: df_outliers_display['Fecha Formateada'] = df_outliers_display['fecha']
        else: df_outliers_display['Fecha Formateada'] = 'N/A'

        if 'importe' in df_outliers_display.columns:
            df_outliers_display['Importe Formateado'] = df_outliers_display['importe'].apply(
                lambda x: f"{moneda_simbolo_oc}{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notna(x) else ""
            )
        else: df_outliers_display['Importe Formateado'] = 'N/A'

        columnas_map_outliers = {
            'Fecha Formateada': 'Fecha',
            'comprobante': 'Comprobante',
            'proveedor': 'Proveedor',
            'descripcion_producto': 'Descripcion Producto',
            'Importe Formateado': 'Importe',
            'gerencia': 'Gerencia',
            'tipocompra': 'Tipocompra'
        }
        df_outliers_renamed = pd.DataFrame()
        for col_original, col_nuevo in columnas_map_outliers.items():
            if col_original in df_outliers_display.columns:
                df_outliers_renamed[col_nuevo] = df_outliers_display[col_original]
            # Si la columna original formateada no existe, intentar con la versión sin formatear (para columnas no fecha/importe)
            elif col_original.replace(" Formateada", "").lower().replace(" ", "_") in df_outliers_display.columns:
                 internal_name = col_original.replace(" Formateada", "").lower().replace(" ", "_")
                 df_outliers_renamed[col_nuevo] = df_outliers_display[internal_name]


        columnas_a_mostrar_final_outliers = ['Fecha', 'Comprobante', 'Proveedor', 'Descripcion Producto', 'Importe', 'Gerencia', 'Tipocompra']
        columnas_existentes_final_outliers = [col for col in columnas_a_mostrar_final_outliers if col in df_outliers_renamed.columns]
        
        if not df_outliers_renamed.empty:
            st.dataframe(df_outliers_renamed[columnas_existentes_final_outliers])
        else:
            st.write("No hay datos de outliers para mostrar.")
        
        st.subheader("Vista de Datos de Órdenes de Compra (Filtrados, Primeras 100)")
        if not df_oc_final_filtrado.empty:
            df_oc_vista_previa = df_oc_final_filtrado.head(100).copy()
            
            if 'fecha' in df_oc_vista_previa.columns:
                if pd.api.types.is_datetime64_any_dtype(df_oc_vista_previa['fecha']):
                    df_oc_vista_previa['fecha_display'] = df_oc_vista_previa['fecha'].dt.strftime('%d/%m/%Y')
                else:
                    try: df_oc_vista_previa['fecha_display'] = pd.to_datetime(df_oc_vista_previa['fecha']).dt.strftime('%d/%m/%Y')
                    except: df_oc_vista_previa['fecha_display'] = df_oc_vista_previa['fecha']
            else: df_oc_vista_previa['fecha_display'] = "N/A"
            
            if 'importe' in df_oc_vista_previa.columns:
                 df_oc_vista_previa['importe_display'] = df_oc_vista_previa['importe'].apply(lambda x: f"{moneda_simbolo_oc}{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            else: df_oc_vista_previa['importe_display'] = "N/A"

            # Seleccionar y renombrar columnas para la vista previa
            df_oc_vista_previa_renamed = pd.DataFrame()
            columnas_map_vista = {
                'fecha_display': 'Fecha', 'comprobante': 'Comprobante', 'proveedor': 'Proveedor',
                'descripcion_producto': 'Descripcion Producto', 'importe_display': 'Importe',
                'moneda': 'Moneda', 'gerencia': 'Gerencia', 'tipocompra': 'Tipocompra'
            }
            columnas_ordenadas_vista = ['Fecha', 'Comprobante', 'Proveedor', 'Descripcion Producto', 'Importe', 'Moneda', 'Gerencia', 'Tipocompra']
            
            for col_original, col_nuevo in columnas_map_vista.items():
                if col_original in df_oc_vista_previa.columns:
                    df_oc_vista_previa_renamed[col_nuevo] = df_oc_vista_previa[col_original]
                # Si la columna formateada no existe, usar la original (para columnas no fecha/importe)
                elif col_original.replace("_display","") in df_oc_vista_previa.columns:
                    df_oc_vista_previa_renamed[col_nuevo] = df_oc_vista_previa[col_original.replace("_display","")]


            # Asegurar el orden y solo columnas existentes
            columnas_existentes_vista = [col for col in columnas_ordenadas_vista if col in df_oc_vista_previa_renamed.columns]
            st.dataframe(df_oc_vista_previa_renamed[columnas_existentes_vista])
        else:
            st.write("No hay datos para mostrar en la vista previa según los filtros aplicados.")
    else:
        st.warning("Seleccione un rango de fechas y moneda válidos para ver el análisis de Órdenes de Compra, o no hay datos para los filtros aplicados.")

with tab_transferencias:
    # ... (Contenido de la pestaña de transferencias, igual que antes) ...
    st.header("Análisis de Transferencias Recibidas")
    df_tr_filtrado_fecha = df_tr.copy() if df_tr is not None else pd.DataFrame()

    if df_tr is not None and 'fecha' in df_tr.columns and not df_tr.empty:
        min_fecha_tr_val = df_tr['fecha'].min()
        max_fecha_tr_val = df_tr['fecha'].max()
        if pd.NaT not in [min_fecha_tr_val, max_fecha_tr_val] and min_fecha_tr_val <= max_fecha_tr_val:
            date_selection_tr = st.sidebar.date_input(
                "Rango o Fecha Única (Transferencias):",
                value=(min_fecha_tr_val.date(), max_fecha_tr_val.date()),
                min_value=min_fecha_tr_val.date(),
                max_value=max_fecha_tr_val.date(),
                key="tr_date_selector"
            )
            if isinstance(date_selection_tr, (tuple, list)) and len(date_selection_tr) == 2:
                fecha_inicio_tr, fecha_fin_tr = date_selection_tr
                df_tr_filtrado_fecha = df_tr[
                    (df_tr['fecha'] >= pd.to_datetime(fecha_inicio_tr)) & 
                    (df_tr['fecha'] <= pd.to_datetime(fecha_fin_tr))
                ]
            elif isinstance(date_selection_tr, date):
                fecha_unica_tr = pd.to_datetime(date_selection_tr)
                df_tr_filtrado_fecha = df_tr[df_tr['fecha'].dt.normalize() == fecha_unica_tr.normalize()]
        else:
            st.sidebar.warning("Fechas base inválidas para filtro de Transferencias.")
    elif df_tr is None:
        st.sidebar.error("Datos de Transferencias no disponibles.")

    if df_tr_filtrado_fecha is not None and not df_tr_filtrado_fecha.empty:
        st.metric("Nº Transferencias (Filtro Aplicado)", len(df_tr_filtrado_fecha))
        
        df_tr_display = df_tr_filtrado_fecha.copy()
        simbolo_moneda_tr_tabla = "ARS$ " 
        if 'fecha' in df_tr_display.columns:
            if pd.api.types.is_datetime64_any_dtype(df_tr_display['fecha']):
                df_tr_display['fecha'] = df_tr_display['fecha'].dt.strftime('%d/%m/%Y')
            else:
                try: df_tr_display['fecha'] = pd.to_datetime(df_tr_display['fecha']).dt.strftime('%d/%m/%Y')
                except: pass
        if 'importe' in df_tr_display.columns:
            df_tr_display['importe'] = df_tr_display['importe'].apply(lambda x: f"{simbolo_moneda_tr_tabla}{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        columnas_display_tr = {
            'desembolso': 'Desembolso', 
            'fecha': 'Fecha',
            'importe': 'Importe'
        }
        df_tr_display = df_tr_display.rename(columns=columnas_display_tr)
        st.dataframe(df_tr_display)
        
        simbolo_moneda_tr_grafico = "ARS$ " 

        col1_tr, col2_tr = st.columns(2)
        with col1_tr:
            st.subheader("Distribución de Importes")
            fig_hist_tr = px.histogram(df_tr_filtrado_fecha, x='importe', marginal="box", title="Distribución de Importes (Transferencias)", color_discrete_sequence=['#00CC96'])
            fig_hist_tr.update_layout(xaxis_title="Importe", yaxis_title="Frecuencia", xaxis_tickprefix=simbolo_moneda_tr_grafico, xaxis_tickformat='.,.0f', height=400)
            st.plotly_chart(fig_hist_tr, use_container_width=True)
        
        with col2_tr:
            st.subheader("Importe Total por Mes")
            if 'fecha' in df_tr_filtrado_fecha.columns and 'importe' in df_tr_filtrado_fecha.columns:
                df_tr_mensual_filtrado = df_tr_filtrado_fecha.set_index('fecha')['importe'].resample('ME').sum().reset_index()
                if not df_tr_mensual_filtrado.empty:
                    df_tr_mensual_grafico = df_tr_mensual_filtrado.rename(columns={'fecha': 'Fecha'})
                    fig_tr_mensual = px.line(df_tr_mensual_grafico, x='Fecha', y='importe', markers=True, title="Importe Mensual de Transferencias")
                    
                    y_values_tr = df_tr_mensual_grafico['importe']
                    if not y_values_tr.empty and pd.notna(y_values_tr.max()) and y_values_tr.max() > 0:
                        num_ticks_tr = 5
                        max_y_tr_val = y_values_tr.max()
                        min_y_tr_val = 0
                        tickvals_tr = np.linspace(min_y_tr_val, max_y_tr_val, num_ticks_tr)
                        tickvals_tr = [v for v in tickvals_tr if pd.notna(v)]
                        if not tickvals_tr: tickvals_tr = [0]
                        ticktext_tr = [format_tick_value(val, simbolo_moneda_tr_grafico) for val in tickvals_tr]
                        fig_tr_mensual.update_layout(yaxis_title="Importe Total Transferido", xaxis_title="Fecha", yaxis_tickvals=tickvals_tr, yaxis_ticktext=ticktext_tr, height=400)
                    else:
                        fig_tr_mensual.update_layout(yaxis_title="Importe Total Transferido", xaxis_title="Fecha", yaxis_tickprefix=simbolo_moneda_tr_grafico, yaxis_tickformat='~s', height=400)
                    st.plotly_chart(fig_tr_mensual, use_container_width=True)
    else:
        st.warning("Seleccione un rango de fechas para ver el análisis de Transferencias o no hay datos para los filtros aplicados.")

# --- ELIMINADA LA PESTAÑA DE CORRELACIÓN ---

st.sidebar.markdown("---")
st.sidebar.markdown("Dashboard Interactivo de Análisis")
st.sidebar.markdown("Creado por: Tamara Monzón Fontano")
st.sidebar.markdown("[Mi Perfil de LinkedIn](https://www.linkedin.com/in/TamaraMonzon)")
st.sidebar.markdown("[Mi Portafolio](https://monzonfontano.netlify.app/)")
st.sidebar.markdown("[Mi Perfil de GitHub](https://github.com/TamaraKaren)")