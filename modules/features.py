import pandas as pd

def create_features(df):
    df = df.copy()
    # Lags
    for i in range(1, 6):
        df[f'Gold_Lag_{i}'] = df['Gold_Price'].shift(i)
        
    # Moving Averages
    df['MA_7'] = df['Gold_Price'].rolling(window=7).mean()
    df['MA_14'] = df['Gold_Price'].rolling(window=14).mean()
    df['MA_30'] = df['Gold_Price'].rolling(window=30).mean()
    
    # Returns and Volatility
    df['Returns'] = df['Gold_Price'].pct_change()
    df['Volatility_7d'] = df['Returns'].rolling(window=7).std() * (252 ** 0.5)
    
    return df
