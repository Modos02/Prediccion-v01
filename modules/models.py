import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def train_arima(train, test):
    # Fit ARIMA model
    model = SARIMAX(train['Gold_Price'], order=(1,1,1))
    model_fit = model.fit(disp=False)
    
    # Forecast
    predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    
    # Metrics
    rmse = np.sqrt(mean_squared_error(test['Gold_Price'], predictions))
    mae = mean_absolute_error(test['Gold_Price'], predictions)
    
    return predictions, rmse, mae

def prepare_lstm_data(data, look_back=30):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back, 0])  # Target is Gold_Price (index 0)
    return np.array(X), np.array(y)

def train_lstm(train_df, test_df, features):
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(train_df[features])
    scaled_test = scaler.transform(test_df[features])
    
    look_back = 30
    X_train, y_train = prepare_lstm_data(scaled_train, look_back)
    X_test, y_test = prepare_lstm_data(scaled_test, look_back)
    
    # Define model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Train model
    model.fit(X_train, y_train, batch_size=32, epochs=10, verbose=0)
    
    # Predict
    predictions = model.predict(X_test)
    
    # Inverse transform
    dummy_pred = np.zeros((len(predictions), len(features)))
    dummy_pred[:, 0] = predictions.flatten()
    inv_predictions = scaler.inverse_transform(dummy_pred)[:, 0]
    
    actual_test_len = len(test_df) - look_back
    y_test_actual = test_df['Gold_Price'].values[look_back:]
    
    rmse = np.sqrt(mean_squared_error(y_test_actual, inv_predictions))
    mae = mean_absolute_error(y_test_actual, inv_predictions)
    
    # We pad the beginning of predictions with NaNs to align with test_df index
    padded_predictions = np.empty(len(test_df))
    padded_predictions[:] = np.nan
    padded_predictions[look_back:] = inv_predictions
    
    return padded_predictions, rmse, mae
