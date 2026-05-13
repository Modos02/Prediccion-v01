import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(page_title="Análisis y Predicción del Precio del Oro", layout="wide", initial_sidebar_state="expanded")

from modules.data_loader import load_and_preprocess_data
from modules.features import create_features
from modules.models import train_arima, train_lstm

# Custom CSS for aesthetic design
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

@st.cache_data
def load_data():
    df = load_and_preprocess_data()
    df = create_features(df)
    return df

st.title("◈ Panel de Predicción del Precio del Oro")

with st.spinner("Cargando y preprocesando datos..."):
    df = load_data()

st.sidebar.header("◉ Navegación")
page = st.sidebar.radio("Ir a", ["▣ Resumen de Datos y AED", "◆ Modelos ARIMA / SARIMA", "◇ Red Neuronal LSTM"])

if page == "▣ Resumen de Datos y AED":
    st.header("▸ Análisis Exploratorio de Datos")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    latest_gold = df['Gold_Price'].iloc[-1]
    prev_gold = df['Gold_Price'].iloc[-2]
    gold_pct = ((latest_gold - prev_gold) / prev_gold) * 100
    
    col1.metric("Último Precio del Oro", f"${latest_gold:,.2f}", f"{gold_pct:.2f}%")
    if 'Bitcoin_Price' in df.columns and not pd.isna(df['Bitcoin_Price'].iloc[-1]):
        col2.metric("Último Precio de Bitcoin", f"${df['Bitcoin_Price'].iloc[-1]:,.2f}")
    if 'VIX' in df.columns and not pd.isna(df['VIX'].iloc[-1]):
        col3.metric("Último VIX", f"{df['VIX'].iloc[-1]:.2f}")
        
    st.subheader("▹ Precio Histórico del Oro")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Gold_Price'], mode='lines', name='Oro', line=dict(color='#FFD700')))
    fig.update_layout(template="plotly_dark", xaxis_title="Fecha", yaxis_title="Precio (USD)", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("▹ Análisis de Correlación")
    corr_df = df[['Gold_Price', 'VIX', 'Bitcoin_Price']].dropna()
    corr = corr_df.corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='Viridis', template="plotly_dark")
    st.plotly_chart(fig_corr, use_container_width=True)

elif page == "◆ Modelos ARIMA / SARIMA":
    st.header("▸ Pronóstico ARIMA / SARIMA")
    st.write("Entrenando el modelo ARIMA con los últimos 1000 días y generando pronóstico...")
    
    if st.button("▶ Ejecutar Modelo ARIMA"):
        with st.spinner("Entrenando modelo..."):
            # Only use the last 1000 rows to speed up ARIMA training
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

elif page == "◇ Red Neuronal LSTM":
    st.header("▸ Pronóstico con Red Neuronal LSTM")
    st.write("Entrenando el modelo LSTM utilizando precios históricos, VIX y Bitcoin como características...")
    
    if st.button("▶ Ejecutar Modelo LSTM"):
        with st.spinner("Entrenando modelo de aprendizaje profundo (esto puede tardar un momento)..."):
            features = ['Gold_Price', 'VIX', 'MA_7', 'MA_30']
            
            # Forward fill missing to avoid NaNs in LSTM
            model_df = df[['Date'] + features].ffill().bfill()
            
            # Use last 2000 points to speed up training if dataset is very large
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
