# ── Importaciones principales ──
# Streamlit para la interfaz web, Pandas para datos, Plotly para gráficas interactivas
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Configuración de la página ──
# Define el título de la pestaña, el layout ancho y la barra lateral abierta por defecto
st.set_page_config(page_title="Análisis y Predicción del Precio del Oro", layout="wide", initial_sidebar_state="expanded")

# ── Módulos internos del proyecto ──
# data_loader: carga y limpia los CSVs  |  features: crea variables derivadas  |  models: entrena ARIMA y LSTM
from modules.data_loader import load_and_preprocess_data
from modules.features import create_features
from modules.models import train_arima, train_lstm

# ── Estilos CSS personalizados ──
# Fondo oscuro, tarjetas con sombra y encabezados dorados para un diseño profesional
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stMetric {
        background-color: #1E2127;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    h1, h2, h3 {
        color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# ── Carga de datos (con caché) ──
# Se cachean los datos para no reprocesar en cada recarga de la página
@st.cache_data
def load_data():
    df = load_and_preprocess_data()
    df = create_features(df)
    return df

# ── Título principal del dashboard ──
st.title("◈ Panel de Predicción del Precio del Oro")

with st.spinner("Cargando y preprocesando datos..."):
    df = load_data()

# ── Barra lateral de navegación ──
# Permite al usuario cambiar entre las tres secciones del dashboard
st.sidebar.header("◉ Navegación")
page = st.sidebar.radio("Ir a", ["▣ Resumen de Datos y AED", "◆ Modelos ARIMA / SARIMA", "◇ Red Neuronal LSTM"])

# ══════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — Resumen de Datos y Análisis Exploratorio (AED)
# Muestra métricas clave, gráfica histórica del oro y matriz de correlación
# ══════════════════════════════════════════════════════════════════════
if page == "▣ Resumen de Datos y AED":
    st.header("▸ Análisis Exploratorio de Datos")
    
    # Tarjetas de métricas: precio más reciente del Oro, Bitcoin y VIX
    col1, col2, col3 = st.columns(3)
    latest_gold = df['Gold_Price'].iloc[-1]
    prev_gold = df['Gold_Price'].iloc[-2]
    gold_pct = ((latest_gold - prev_gold) / prev_gold) * 100
    
    col1.metric("Último Precio del Oro", f"${latest_gold:,.2f}", f"{gold_pct:.2f}%")
    if 'Bitcoin_Price' in df.columns and not pd.isna(df['Bitcoin_Price'].iloc[-1]):
        col2.metric("Último Precio de Bitcoin", f"${df['Bitcoin_Price'].iloc[-1]:,.2f}")
    if 'VIX' in df.columns and not pd.isna(df['VIX'].iloc[-1]):
        col3.metric("Último VIX", f"{df['VIX'].iloc[-1]:.2f}")
        
    # Gráfica de línea con la evolución histórica del precio del oro
    st.subheader("▹ Precio Histórico del Oro")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Gold_Price'], mode='lines', name='Oro', line=dict(color='#FFD700')))
    fig.update_layout(template="plotly_dark", xaxis_title="Fecha", yaxis_title="Precio (USD)", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    # Mapa de calor: correlación entre Oro, VIX y Bitcoin
    st.subheader("▹ Análisis de Correlación")
    corr_df = df[['Gold_Price', 'VIX', 'Bitcoin_Price']].dropna()
    corr = corr_df.corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='Viridis', template="plotly_dark")
    st.plotly_chart(fig_corr, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Modelo ARIMA / SARIMA
# Entrena un modelo estadístico ARIMA(1,1,1) con los últimos 1000 días
# y compara las predicciones con los datos reales de prueba
# ══════════════════════════════════════════════════════════════════════
elif page == "◆ Modelos ARIMA / SARIMA":
    st.header("▸ Pronóstico ARIMA / SARIMA")
    st.write("Entrenando el modelo ARIMA con los últimos 1000 días y generando pronóstico...")
    
    if st.button("▶ Ejecutar Modelo ARIMA"):
        with st.spinner("Entrenando modelo..."):
            # Se usan solo los últimos 1000 registros para acelerar el entrenamiento
            train_df = df.iloc[-1000:].reset_index(drop=True)
            train_size = int(len(train_df) * 0.8)
            train = train_df.iloc[:train_size]
            test = train_df.iloc[train_size:]
            
            predictions, rmse, mae = train_arima(train, test)
            
            col1, col2 = st.columns(2)
            col1.metric("RMSE", f"{rmse:.2f}")
            col2.metric("MAE", f"{mae:.2f}")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train['Date'].iloc[-500:], y=train['Gold_Price'].iloc[-500:], mode='lines', name='Entrenamiento'))
            fig.add_trace(go.Scatter(x=test['Date'], y=test['Gold_Price'], mode='lines', name='Prueba Real'))
            fig.add_trace(go.Scatter(x=test['Date'], y=predictions, mode='lines', name='Predicciones ARIMA', line=dict(color='red')))
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Red Neuronal LSTM
# Entrena una red LSTM (Long Short-Term Memory) con características:
# Gold_Price, VIX, MA_7 y MA_30.  Usa los últimos 2000 puntos.
# ══════════════════════════════════════════════════════════════════════
elif page == "◇ Red Neuronal LSTM":
    st.header("▸ Pronóstico con Red Neuronal LSTM")
    st.write("Entrenando el modelo LSTM utilizando precios históricos, VIX y Bitcoin como características...")
    
    if st.button("▶ Ejecutar Modelo LSTM"):
        with st.spinner("Entrenando modelo de aprendizaje profundo (esto puede tardar un momento)..."):
            features = ['Gold_Price', 'VIX', 'MA_7', 'MA_30']
            
            # Relleno hacia adelante y atrás para evitar NaN en la red neuronal
            model_df = df[['Date'] + features].ffill().bfill()
            
            # Se limitan a 2000 puntos para agilizar el entrenamiento
            model_df = model_df.iloc[-2000:].reset_index(drop=True)
            
            train_size = int(len(model_df) * 0.8)
            train = model_df.iloc[:train_size]
            test = model_df.iloc[train_size:]
            
            predictions, rmse, mae = train_lstm(train, test, features)
            
            col1, col2 = st.columns(2)
            col1.metric("RMSE", f"{rmse:.2f}")
            col2.metric("MAE", f"{mae:.2f}")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train['Date'].iloc[-500:], y=train['Gold_Price'].iloc[-500:], mode='lines', name='Entrenamiento'))
            fig.add_trace(go.Scatter(x=test['Date'], y=test['Gold_Price'], mode='lines', name='Prueba Real'))
            fig.add_trace(go.Scatter(x=test['Date'], y=predictions, mode='lines', name='Predicciones LSTM', line=dict(color='orange')))
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
