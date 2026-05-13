import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(page_title="Gold Price Analysis & Prediction", layout="wide", initial_sidebar_state="expanded")

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

st.title("🥇 Gold Price Prediction Dashboard")

with st.spinner("Loading and preprocessing data..."):
    df = load_data()

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Data Overview & EDA", "ARIMA / SARIMA Models", "LSTM Neural Network"])

if page == "Data Overview & EDA":
    st.header("Exploratory Data Analysis")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    latest_gold = df['Gold_Price'].iloc[-1]
    prev_gold = df['Gold_Price'].iloc[-2]
    gold_pct = ((latest_gold - prev_gold) / prev_gold) * 100
    
    col1.metric("Latest Gold Price", f"${latest_gold:,.2f}", f"{gold_pct:.2f}%")
    if 'Bitcoin_Price' in df.columns and not pd.isna(df['Bitcoin_Price'].iloc[-1]):
        col2.metric("Latest Bitcoin Price", f"${df['Bitcoin_Price'].iloc[-1]:,.2f}")
    if 'VIX' in df.columns and not pd.isna(df['VIX'].iloc[-1]):
        col3.metric("Latest VIX", f"{df['VIX'].iloc[-1]:.2f}")
        
    st.subheader("Historical Gold Price")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Gold_Price'], mode='lines', name='Gold', line=dict(color='#FFD700')))
    fig.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="Price (USD)", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Correlation Analysis")
    corr_df = df[['Gold_Price', 'VIX', 'Bitcoin_Price']].dropna()
    corr = corr_df.corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='Viridis', template="plotly_dark")
    st.plotly_chart(fig_corr, use_container_width=True)

elif page == "ARIMA / SARIMA Models":
    st.header("ARIMA / SARIMA Forecasting")
    st.write("Training ARIMA model on the latest 1000 days and forecasting...")
    
    if st.button("Run ARIMA Model"):
        with st.spinner("Training model..."):
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
            fig.add_trace(go.Scatter(x=train['Date'].iloc[-500:], y=train['Gold_Price'].iloc[-500:], mode='lines', name='Train'))
            fig.add_trace(go.Scatter(x=test['Date'], y=test['Gold_Price'], mode='lines', name='Actual Test'))
            fig.add_trace(go.Scatter(x=test['Date'], y=predictions, mode='lines', name='ARIMA Predictions', line=dict(color='red')))
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

elif page == "LSTM Neural Network":
    st.header("LSTM Neural Network Forecasting")
    st.write("Training LSTM model using historical prices, VIX, and Bitcoin as features...")
    
    if st.button("Run LSTM Model"):
        with st.spinner("Training deep learning model (this may take a minute)..."):
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
            fig.add_trace(go.Scatter(x=train['Date'].iloc[-500:], y=train['Gold_Price'].iloc[-500:], mode='lines', name='Train'))
            fig.add_trace(go.Scatter(x=test['Date'], y=test['Gold_Price'], mode='lines', name='Actual Test'))
            fig.add_trace(go.Scatter(x=test['Date'], y=predictions, mode='lines', name='LSTM Predictions', line=dict(color='orange')))
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
