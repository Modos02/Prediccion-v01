# ── Módulo de modelos predictivos ──
# Contiene las funciones de entrenamiento y predicción para:
#   • ARIMA / SARIMA  (modelo estadístico de series de tiempo)
#   • LSTM            (red neuronal recurrente de memoria a largo-corto plazo)
# Incluye evaluación, intervalos de confianza y predicción futura.
import pandas as pd
import numpy as np
import time
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler


# ── Entrenamiento ARIMA ──
# Ajusta un modelo SARIMAX con orden configurable y genera predicciones con intervalos de confianza
def train_arima(train, test, order=(1, 1, 1)):
    start_time = time.time()

    model = SARIMAX(train['Gold_Price'], order=order)
    model_fit = model.fit(disp=False)

    # Pronóstico con intervalos de confianza al 95%
    forecast = model_fit.get_forecast(steps=len(test))
    predictions = forecast.predicted_mean.values
    conf_int = forecast.conf_int(alpha=0.05)
    lower_ci = conf_int.iloc[:, 0].values
    upper_ci = conf_int.iloc[:, 1].values

    # Métricas de error
    rmse = np.sqrt(mean_squared_error(test['Gold_Price'], predictions))
    mae = mean_absolute_error(test['Gold_Price'], predictions)
    mape = np.mean(np.abs((test['Gold_Price'].values - predictions) / test['Gold_Price'].values)) * 100

    elapsed = time.time() - start_time

    return predictions, rmse, mae, mape, elapsed, lower_ci, upper_ci


# ── Predicción futura ARIMA ──
# Entrena con todos los datos disponibles y genera pronóstico para N días futuros
def predict_future_arima(df, order=(1, 1, 1), horizon_days=252):
    start_time = time.time()

    model = SARIMAX(df['Gold_Price'], order=order)
    model_fit = model.fit(disp=False)

    # En lugar de usar la media predicha (línea recta), generamos un camino simulado realista
    np.random.seed(42) # Semilla para consistencia visual
    predictions = model_fit.simulate(nsimulations=horizon_days, anchor='end').values
    
    # Ya no usamos intervalos de confianza porque mostraremos el camino proyectado
    lower_ci = np.zeros(horizon_days)
    upper_ci = np.zeros(horizon_days)

    # Crear fechas futuras (días hábiles)
    last_date = df['Date'].iloc[-1]
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=horizon_days, freq='B'
    )

    elapsed = time.time() - start_time

    return future_dates, predictions, lower_ci, upper_ci, elapsed


# ── Preparación de datos para LSTM ──
# Genera ventanas deslizantes de tamaño look_back para entrada (X) y salida (y)
def prepare_lstm_data(data, look_back=30):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back, 0])  # El objetivo es Gold_Price (índice 0)
    return np.array(X), np.array(y)


# ── Entrenamiento LSTM ──
# Escala los datos, construye la red neuronal LSTM con EarlyStopping y genera predicciones
def train_lstm(train_df, test_df, features, epochs=20, look_back=30):
    start_time = time.time()

    # Escalar datos al rango [0, 1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(train_df[features])
    scaled_test = scaler.transform(test_df[features])

    X_train, y_train = prepare_lstm_data(scaled_train, look_back)
    X_test, y_test = prepare_lstm_data(scaled_test, look_back)

    # Lazy loading de TensorFlow para evitar errores de importación en el arranque
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        from tensorflow.keras.callbacks import EarlyStopping
    except ImportError:
        raise ImportError("No se pudo cargar TensorFlow. Asegúrate de que esté instalado en requirements.txt")

    # Definir la arquitectura de la red neuronal
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Early stopping para evitar sobreajuste
    early_stop = EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)

    model.fit(X_train, y_train, batch_size=32, epochs=epochs, verbose=0, callbacks=[early_stop])

    # Realizar predicciones
    predictions = model.predict(X_test, verbose=0)

    # Invertir la transformación para obtener precios reales en USD
    dummy_pred = np.zeros((len(predictions), len(features)))
    dummy_pred[:, 0] = predictions.flatten()
    inv_predictions = scaler.inverse_transform(dummy_pred)[:, 0]

    y_test_actual = test_df['Gold_Price'].values[look_back:]

    rmse = np.sqrt(mean_squared_error(y_test_actual, inv_predictions))
    mae = mean_absolute_error(y_test_actual, inv_predictions)
    mape = np.mean(np.abs((y_test_actual - inv_predictions) / y_test_actual)) * 100

    # Rellenar el inicio con NaN para alinear las predicciones con el índice de test_df
    padded_predictions = np.empty(len(test_df))
    padded_predictions[:] = np.nan
    padded_predictions[look_back:] = inv_predictions

    elapsed = time.time() - start_time

    return padded_predictions, rmse, mae, mape, elapsed, model, scaler


# ── Predicción futura LSTM ──
# Usa predicción recursiva para generar pronósticos más allá de los datos disponibles
def predict_future_lstm(df, features, model, scaler, horizon_days=252, look_back=30):
    start_time = time.time()

    scaled_data = scaler.transform(df[features].values)

    # Tomar los últimos look_back días como punto de partida
    current_input = scaled_data[-look_back:].copy()

    future_predictions = []

    # Lazy loading de TensorFlow
    try:
        from tensorflow.keras.models import Sequential
    except ImportError:
        pass # El modelo ya debería estar cargado si llegamos aquí
    
    for i in range(horizon_days):
        input_reshaped = current_input.reshape(1, look_back, len(features))
        pred = model.predict(input_reshaped, verbose=0)[0, 0]

        # Crear la siguiente fila de entrada (desplazar y agregar predicción)
        next_row = current_input[-1].copy()
        next_row[0] = pred  # Gold_Price es el índice 0

        current_input = np.vstack([current_input[1:], next_row])
        future_predictions.append(pred)

    # Invertir la transformación para obtener precios en USD
    future_predictions = np.array(future_predictions)
    dummy = np.zeros((len(future_predictions), len(features)))
    dummy[:, 0] = future_predictions
    inv_predictions = scaler.inverse_transform(dummy)[:, 0]

    # Crear fechas futuras (días hábiles)
    last_date = df['Date'].iloc[-1]
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=horizon_days, freq='B'
    )

    elapsed = time.time() - start_time

    return future_dates, inv_predictions, elapsed
