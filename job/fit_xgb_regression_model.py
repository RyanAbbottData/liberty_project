"""
File that contains functions for fitting the project's model
"""
# Third-party imports
import pandas as pd
import xgboost as xgb


def fit_xgb_regression_model(df_path,
                             model_save_path):
    """
        Train and save an XGBoost regression model for temperature forecast.

        This function loads weather data from a CSV file, performs feature engineering
        to extract time-based features, creates a model to predict temperature 15 minutes in the future based on
        hour, month, then saves the trained model.

        Parameters
        ----------
        df_path : str
            Path to the CSV file containing weather data. The file must include 'time'
            and 'temperature_2m' columns.

        model_save_path : str
            Path where the trained XGBoost model will be saved.

        Returns
        -------
        xgb.XGBRegressor
            The trained XGBoost regression model.

        Notes
        -----
        - The function converts ISO 8601 timestamps to datetime objects
        - Feature engineering includes:
          - Extracting time of day as HHMM integer (e.g., 1430 for 2:30 PM)
          - Extracting hour and month as separate features
          - Creating a lagged feature for temperature from 15 minutes ago
        - The model uses only 'hour', 'month', and 'previous_15_min_temp' as features
        - The target variable is 'temperature_2m'
        - The model is trained on the entire dataset without train/test splitting
    """
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
    df['previous_30_min_temp'] = df['temperature_2m'].shift(2)
    df['previous_45_min_temp'] = df['temperature_2m'].shift(3)
    df['previous_1_hour_temp'] = df['temperature_2m'].shift(4)
    df['previous_15_min_dew_point'] = df['dew_point_2m'].shift(1)

    # Dropping any NaN values
    df = df.dropna()

    # Separating x, y, training and testing data
    x_cols = ['hour',
              'month',
              'previous_15_min_temp',
              'previous_30_min_temp',
              'previous_45_min_temp',
              'previous_1_hour_temp',
              'previous_15_min_dew_point']
    y_col = ['temperature_2m']

    x = df[x_cols]
    y = df[y_col]

    # Create XGBoost classifier
    model = xgb.XGBRegressor()

    # Fit model to November, December, and January data
    model.fit(x, y)

    model.save_model(model_save_path)

    return model
