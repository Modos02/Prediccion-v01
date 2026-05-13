# ── Módulo de carga y preprocesamiento de datos ──
# Funciones para leer los CSVs con formatos numéricos español e inglés,
# limpiar valores y unificar todo en un solo DataFrame.
import pandas as pd
import numpy as np

# Convierte texto con formato numérico español (punto=miles, coma=decimal) a float
def clean_spanish_number(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    # Quitar puntos (separador de miles) y reemplazar coma por punto (decimal)
    val = str(val).replace('.', '').replace(',', '.')
    try:
        return float(val)
    except:
        return np.nan

# Convierte texto con formato numérico inglés (coma=miles) a float
def clean_english_number(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    # Quitar comas (separador de miles)
    val = str(val).replace(',', '')
    try:
        return float(val)
    except:
        return np.nan

# ── Función principal: carga los 3 CSVs, limpia y fusiona ──
def load_and_preprocess_data():
    # Cargar datos del Oro
    df_gold = pd.read_csv('Datos históricos Oro 2000 AL 2026.csv', skiprows=[1])
    df_gold['Date'] = pd.to_datetime(df_gold['Fecha'], format='%d.%m.%Y', errors='coerce')
    df_gold['Gold_Price'] = df_gold['Último'].apply(clean_spanish_number)
    df_gold = df_gold[['Date', 'Gold_Price']].dropna(subset=['Date'])
    
    # Cargar datos del índice VIX (volatilidad)
    df_vix = pd.read_csv('Datos históricos del S&P 500 VIX.csv')
    df_vix['Date'] = pd.to_datetime(df_vix['Fecha'], format='%d.%m.%Y', errors='coerce')
    df_vix['VIX'] = df_vix['Último'].apply(clean_spanish_number)
    df_vix = df_vix[['Date', 'VIX']].dropna(subset=['Date'])
    
    # Cargar datos de Bitcoin
    df_btc = pd.read_csv('DATA HISTORICA BITCOIN.csv')
    df_btc['Date'] = pd.to_datetime(df_btc['Date'], errors='coerce')
    df_btc['Bitcoin_Price'] = df_btc['Price'].apply(clean_english_number)
    df_btc = df_btc[['Date', 'Bitcoin_Price']].dropna(subset=['Date'])
    
    # Fusionar los tres datasets por fecha
    df = pd.merge(df_gold, df_vix, on='Date', how='outer')
    df = pd.merge(df, df_btc, on='Date', how='outer')
    
    # Ordenar por fecha
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Rellenar valores faltantes hacia adelante
    df.ffill(inplace=True)
    
    # Eliminar filas donde el precio del Oro sigue siendo NaN
    df.dropna(subset=['Gold_Price'], inplace=True)
    
    return df
