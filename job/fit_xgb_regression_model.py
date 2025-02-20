# Standard library imports
from datetime import datetime
import warnings

# Third-party imports
import pandas as pd
import requests
import xgboost as xgb


def fit_xgb_regression_model(df_path,
                             model_save_path):
    # Loading dataset with newest data
    df = pd.read_csv(df_path)

    # Converting ISO 8162 to Unix timestamp for python operations
    df['time'] = pd.to_datetime(df['time'])

    # Converting ISO 8162
    df['time_of_day'] = [int(t.time().strftime("%H%M")) for t in df['time']]

    # Extracting hour and month from timestamp
    df['hour'] = [t.hour for t in df['time']]
    df['month'] = [t.month for t in df['time']]

    # getting the temperature from the previous 15 minutes
    df['previous_15_min_temp'] = df['temperature_2m'].shift(1)

    # Separating x, y, training and testing data
    x_cols = ['hour', 'month', 'previous_15_min_temp']
    y_col = ['temperature_2m']

    x = df[x_cols]
    y = df[y_col]

    # Create XGBoost classifier
    model = xgb.XGBRegressor()

    # Fit model to November, December, and January data
    model.fit(x, y)

    model.save_model(model_save_path)

    return model