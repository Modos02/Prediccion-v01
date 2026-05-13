import pandas as pd
import numpy as np

def clean_spanish_number(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    # Remove dots (thousands separator) and replace comma with dot (decimal separator)
    val = str(val).replace('.', '').replace(',', '.')
    try:
        return float(val)
    except:
        return np.nan

def clean_english_number(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    # Remove commas (thousands separator)
    val = str(val).replace(',', '')
    try:
        return float(val)
    except:
        return np.nan

def load_and_preprocess_data():
    # Load Gold Data
    df_gold = pd.read_csv('Datos históricos Oro 2000 AL 2026.csv', skiprows=[1])
    df_gold['Date'] = pd.to_datetime(df_gold['Fecha'], format='%d.%m.%Y', errors='coerce')
    df_gold['Gold_Price'] = df_gold['Último'].apply(clean_spanish_number)
    df_gold = df_gold[['Date', 'Gold_Price']].dropna(subset=['Date'])
    
    # Load VIX Data
    df_vix = pd.read_csv('Datos históricos del S&P 500 VIX.csv')
    df_vix['Date'] = pd.to_datetime(df_vix['Fecha'], format='%d.%m.%Y', errors='coerce')
    df_vix['VIX'] = df_vix['Último'].apply(clean_spanish_number)
    df_vix = df_vix[['Date', 'VIX']].dropna(subset=['Date'])
    
    # Load Bitcoin Data
    df_btc = pd.read_csv('DATA HISTORICA BITCOIN.csv')
    df_btc['Date'] = pd.to_datetime(df_btc['Date'], errors='coerce')
    df_btc['Bitcoin_Price'] = df_btc['Price'].apply(clean_english_number)
    df_btc = df_btc[['Date', 'Bitcoin_Price']].dropna(subset=['Date'])
    
    # Merge datasets
    df = pd.merge(df_gold, df_vix, on='Date', how='outer')
    df = pd.merge(df, df_btc, on='Date', how='outer')
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Fill NA using forward fill
    df.ffill(inplace=True)
    
    # Drop rows where Gold_Price is still NaN
    df.dropna(subset=['Gold_Price'], inplace=True)
    
    return df
