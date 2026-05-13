# ── Módulo de ingeniería de características ──
# Crea variables derivadas (rezagos, promedios móviles, retornos y volatilidad)
# a partir del precio del oro para alimentar los modelos predictivos.
import pandas as pd

def create_features(df):
    df = df.copy()
    # Rezagos (lags): precio del oro de los últimos 1 a 5 días
    for i in range(1, 6):
        df[f'Gold_Lag_{i}'] = df['Gold_Price'].shift(i)
        
    # Promedios móviles de 7, 14 y 30 días
    df['MA_7'] = df['Gold_Price'].rolling(window=7).mean()
    df['MA_14'] = df['Gold_Price'].rolling(window=14).mean()
    df['MA_30'] = df['Gold_Price'].rolling(window=30).mean()
    
    # Retornos porcentuales diarios y volatilidad anualizada a 7 días
    df['Returns'] = df['Gold_Price'].pct_change()
    df['Volatility_7d'] = df['Returns'].rolling(window=7).std() * (252 ** 0.5)
    
    return df
