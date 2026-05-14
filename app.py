import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ── Importaciones de módulos internos ──
from modules.data_loader import load_and_preprocess_data
from modules.features import create_features
from modules.models import (
    train_arima, predict_future_arima, 
    train_lstm, predict_future_lstm
)
from styles import (
    CSS, FONT_AWESOME, GOOGLE_FONTS, 
    section_header, metric_card, metric_row, 
    info_box, warn_box, trend_badge
)

# ── Configuración de la página ──
st.set_page_config(
    page_title="Gold Predict Pro | Análisis Financiero", 
    page_icon="📈",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Inyectar estilos
st.markdown(FONT_AWESOME, unsafe_allow_html=True)
st.markdown(GOOGLE_FONTS, unsafe_allow_html=True)
st.markdown(CSS, unsafe_allow_html=True)

# ── Carga de datos ──
@st.cache_data(show_spinner=False)
def get_data():
    df = load_and_preprocess_data()
    df = create_features(df)
    return df

with st.spinner("🚀 Inicializando plataforma financiera..."):
    df = get_data()

# ── Sidebar de Navegación y Configuración ──
with st.sidebar:
    st.markdown(f'<div style="text-align: center; padding: 20px 0;"><h1 style="color: #3b82f6 !important; font-size: 1.8rem !important; margin:0;">GOLD<span style="color: #f1f5f9;">PREDICT</span></h1><p style="color: #64748b; font-size: 0.7rem; letter-spacing: 2px; font-weight: 700;">PRO ANALYTICS v1.0</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    page = st.sidebar.radio("MENÚ PRINCIPAL", [
        "📊 Panel de Control & AED", 
        "📈 Modelo Estadístico ARIMA", 
        "🧠 Red Neuronal LSTM",
        "🔮 Proyección a 10 Años"
    ])
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### ⚙️ CONFIGURACIÓN")
    
    if "ARIMA" in page:
        p = st.slider("Orden p (Auto-regresivo)", 0, 5, 1)
        d = st.slider("Orden d (Integrado)", 0, 2, 1)
        q = st.slider("Orden q (Media Móvil)", 0, 5, 1)
        st.session_state.arima_order = (p, d, q)
    elif "LSTM" in page:
        epochs = st.slider("Épocas de entrenamiento", 5, 50, 15)
        look_back = st.slider("Ventana de tiempo (días)", 10, 60, 30)
        st.session_state.lstm_config = {"epochs": epochs, "look_back": look_back}
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f'<div style="color: #475569; font-size: 0.7rem;">Última actualización:<br>{datetime.now().strftime("%d/%m/%Y %H:%M")}</div>', unsafe_allow_html=True)

# ── Lógica de Páginas ──

# 📊 PANEL DE CONTROL & AED
if page == "📊 Panel de Control & AED":
    st.markdown(section_header("fa-solid fa-chart-line", "Análisis Exploratorio de Datos"), unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Visualización en tiempo real del mercado del oro y variables correlacionadas. Datos históricos desde el año 2000.</p>', unsafe_allow_html=True)
    
    # Métricas Principales
    latest_gold = df['Gold_Price'].iloc[-1]
    prev_gold = df['Gold_Price'].iloc[-2]
    gold_pct = ((latest_gold - prev_gold) / prev_gold) * 100
    
    latest_vix = df['VIX'].iloc[-1] if 'VIX' in df.columns else 0
    latest_btc = df['Bitcoin_Price'].iloc[-1] if 'Bitcoin_Price' in df.columns else 0
    
    cards = [
        metric_card("fa-solid fa-coins", "Precio Oro (USD)", f"${latest_gold:,.2f}", f"{gold_pct:+.2f}%", gold_pct >= 0),
        metric_card("fa-solid fa-arrow-trend-up", "Índice VIX", f"{latest_vix:.2f}", "Volatilidad", True),
        metric_card("fa-brands fa-bitcoin", "Bitcoin (Ref)", f"${latest_btc:,.0f}", "Mercado Crypto", True)
    ]
    st.markdown(metric_row(cards), unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Histórico", "🔍 Correlación", "📋 Datos Crudos"])
    
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Gold_Price'], mode='lines', name='Precio Oro', line=dict(color='#3b82f6', width=2)))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_30'], mode='lines', name='Media Móvil (30d)', line=dict(color='#f59e0b', width=1, dash='dot')))
        fig.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, color='#64748b'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#64748b'),
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        col_c1, col_c2 = st.columns([1, 2])
        with col_c1:
            st.markdown("### 🛰️ Factores de Influencia")
            st.write("Análisis de cómo el precio del oro reacciona ante la volatilidad del mercado (VIX) y activos digitales (Bitcoin).")
            st.markdown(info_box("El oro suele actuar como activo refugio cuando el VIX sube."))
        with col_c2:
            corr_df = df[['Gold_Price', 'VIX', 'Bitcoin_Price']].dropna()
            corr = corr_df.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='Blues', template="plotly_dark")
            fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig_corr, use_container_width=True)
            
    with tab3:
        st.markdown(f"**Total de registros detectados:** `{len(df):,}`")
        st.dataframe(df.tail(100), use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Dataset Completo (CSV)", csv, "datos_oro_procesados.csv", "text/csv")

# 📈 MODELO ESTADÍSTICO ARIMA
elif page == "📈 Modelo Estadístico ARIMA":
    st.markdown(section_header("fa-solid fa-chart-simple", "Pronóstico Estadístico ARIMA"), unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Modelo Auto-regresivo Integrado de Media Móvil. Ideal para capturar tendencias y estacionalidad a corto y mediano plazo.</p>', unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns([1, 3])
    with col_a1:
        st.markdown("### 🧪 Entrenamiento")
        st.write("Se utiliza el 80% de los datos para entrenamiento y 20% para validación.")
        if st.button("🚀 Ejecutar Simulación", key="run_arima"):
            with st.spinner("Ajustando parámetros estadísticos..."):
                train_df = df.iloc[-1500:].reset_index(drop=True)
                train_size = int(len(train_df) * 0.8)
                train = train_df.iloc[:train_size]
                test = train_df.iloc[train_size:]
                
                order = st.session_state.get('arima_order', (1,1,1))
                preds, rmse, mae, mape, elapsed, lower, upper = train_arima(train, test, order)
                
                st.session_state.arima_results = {
                    "preds": preds, "rmse": rmse, "mae": mae, "mape": mape, 
                    "elapsed": elapsed, "lower": lower, "upper": upper,
                    "test": test, "train": train
                }
        
        if "arima_results" in st.session_state:
            res = st.session_state.arima_results
            st.markdown(f"**Tiempo:** `{res['elapsed']:.2f}s`")
            st.metric("Precisión (MAPE)", f"{100-res['mape']:.2f}%")
            st.metric("Error (RMSE)", f"{res['rmse']:.2f}")

    with col_a2:
        if "arima_results" in st.session_state:
            res = st.session_state.arima_results
            fig = go.Figure()
            # Entrenamiento
            fig.add_trace(go.Scatter(x=res['train']['Date'].iloc[-200:], y=res['train']['Gold_Price'].iloc[-200:], name='Histórico', line=dict(color='#64748b')))
            # Real
            fig.add_trace(go.Scatter(x=res['test']['Date'], y=res['test']['Gold_Price'], name='Real', line=dict(color='#f1f5f9')))
            # Predicción
            fig.add_trace(go.Scatter(x=res['test']['Date'], y=res['preds'], name='ARIMA', line=dict(color='#3b82f6', width=3)))
            # Intervalo de confianza
            fig.add_trace(go.Scatter(x=res['test']['Date'], y=res['upper'], fill=None, mode='lines', line_color='rgba(59,130,246,0)', showlegend=False))
            fig.add_trace(go.Scatter(x=res['test']['Date'], y=res['lower'], fill='tonexty', mode='lines', line_color='rgba(59,130,246,0)', fillcolor='rgba(59,130,246,0.1)', name='Confianza 95%'))
            
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Presiona el botón para iniciar el análisis estadístico.")

# 🧠 RED NEURONAL LSTM
elif page == "🧠 Red Neuronal LSTM":
    st.markdown(section_header("fa-solid fa-brain", "Red Neuronal LSTM (Deep Learning)"), unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Long Short-Term Memory. Una arquitectura de red neuronal recurrente capaz de aprender dependencias a largo plazo en series financieras complejas.</p>', unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([1, 3])
    with col_l1:
        st.markdown("### 🧬 Aprendizaje Profundo")
        st.write("Este modelo analiza patrones multivariables incluyendo VIX y medias móviles.")
        if st.button("🔥 Entrenar Cerebro IA", key="run_lstm"):
            with st.spinner("La IA está analizando los patrones del mercado..."):
                features = ['Gold_Price', 'VIX', 'MA_7', 'MA_30']
                model_df = df[['Date'] + features].ffill().bfill().iloc[-2000:].reset_index(drop=True)
                
                train_size = int(len(model_df) * 0.8)
                train = model_df.iloc[:train_size]
                test = model_df.iloc[train_size:]
                
                config = st.session_state.get('lstm_config', {"epochs": 15, "look_back": 30})
                preds, rmse, mae, mape, elapsed, model, scaler = train_lstm(train, test, features, **config)
                
                st.session_state.lstm_results = {
                    "preds": preds, "rmse": rmse, "mae": mae, "mape": mape, 
                    "elapsed": elapsed, "test": test, "train": train
                }
        
        if "lstm_results" in st.session_state:
            res = st.session_state.lstm_results
            st.markdown(f"**Tiempo de entrenamiento:** `{res['elapsed']:.1f}s`")
            st.metric("Puntuación de Precisión", f"{100-res['mape']:.2f}%")
            st.metric("MAE (Error Absoluto)", f"{res['mae']:.2f}")

    with col_l2:
        if "lstm_results" in st.session_state:
            res = st.session_state.lstm_results
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=res['train']['Date'].iloc[-200:], y=res['train']['Gold_Price'].iloc[-200:], name='Entrenamiento', line=dict(color='#64748b')))
            fig.add_trace(go.Scatter(x=res['test']['Date'], y=res['test']['Gold_Price'], name='Real', line=dict(color='#f1f5f9')))
            fig.add_trace(go.Scatter(x=res['test']['Date'], y=res['preds'], name='LSTM Prediction', line=dict(color='#22c55e', width=3)))
            
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Configura los parámetros en la barra lateral y presiona 'Entrenar Cerebro IA'.")

# 🔮 PROYECCIÓN A 10 AÑOS
elif page == "🔮 Proyección a 10 Años":
    st.markdown(section_header("fa-solid fa-wand-magic-sparkles", "Proyección de Futuro a 10 Años"), unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Algoritmo de simulación a largo plazo (2,520 días bursátiles). Nota: Las proyecciones a muy largo plazo están sujetas a alta incertidumbre económica.</p>', unsafe_allow_html=True)
    
    st.markdown(warn_box("Las predicciones a 10 años son estimaciones basadas puramente en tendencias históricas y no consideran eventos macroeconómicos impredecibles."))
    
    if st.button("✨ GENERAR PROYECCIÓN DE DÉCADA", key="run_future"):
        with st.spinner("Calculando trayectoria del mercado hasta el año 2036..."):
            # Usar ARIMA para proyección a largo plazo por estabilidad
            order = st.session_state.get('arima_order', (1,1,1))
            horizon = 252 * 10 # 10 años aprox
            future_dates, future_preds, lower, upper, elapsed = predict_future_arima(df, order, horizon)
            
            fig = go.Figure()
            # Datos históricos últimos 2 años
            hist_subset = df.iloc[-500:]
            fig.add_trace(go.Scatter(x=hist_subset['Date'], y=hist_subset['Gold_Price'], name='Precio Actual', line=dict(color='#64748b')))
            # Proyección
            fig.add_trace(go.Scatter(x=future_dates, y=future_preds, name='Tendencia Proyectada', line=dict(color='#3b82f6', width=4)))
            # Intervalo
            fig.add_trace(go.Scatter(x=future_dates, y=upper, fill=None, mode='lines', line_color='rgba(59,130,246,0)', showlegend=False))
            fig.add_trace(go.Scatter(x=future_dates, y=lower, fill='tonexty', mode='lines', line_color='rgba(59,130,246,0)', fillcolor='rgba(59,130,246,0.1)', name='Rango de Probabilidad'))
            
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Año de Proyección", yaxis_title="Precio Estimado (USD)",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Resumen de Proyección
            final_price = future_preds[-1]
            growth = ((final_price - latest_gold) / latest_gold) * 100
            trend = "ALCISTA ↑" if growth > 0 else "BAJISTA ↓"
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                st.markdown(f"### Precio Est. 2036")
                st.markdown(f"<h2 style='color:#3b82f6'>${final_price:,.2f}</h2>", unsafe_allow_html=True)
            with col_f2:
                st.markdown(f"### Variación Total")
                st.markdown(f"<h2 style='color:{'#22c55e' if growth > 0 else '#ef4444'}'>{growth:+.1f}%</h2>", unsafe_allow_html=True)
            with col_f3:
                st.markdown(f"### Tendencia Dominante")
                st.markdown(f"<div>{trend_badge('up' if growth > 0 else 'down', trend)}</div>", unsafe_allow_html=True)

# ── Footer ──
st.markdown(f'''<div class="app-footer">
    GOLD PREDICT PRO &copy; {datetime.now().year} | Análisis Cuantitativo de Metales Preciosos<br>
    Desarrollado con Streamlit, TensorFlow y Plotly
</div>''', unsafe_allow_html=True)
