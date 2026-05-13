import sys
import os
sys.path.append('d:/Gravity/Arima')
from modules.data_loader import load_and_preprocess_data

try:
    df = load_and_preprocess_data()
    print("Data loaded successfully!")
    print(df.head())
    print("Length:", len(df))
    print(df.tail())
except Exception as e:
    import traceback
    traceback.print_exc()
