"""
The main file of the project that will run the pipeline
"""
# Standard library imports
from datetime import timedelta
import warnings
import logging
from time import sleep

# Third-party imports
import pandas as pd
import numpy

# Project imports
from job.fit_xgb_regression_model import fit_xgb_regression_model
from job.get_15_minutely_temp_data import get_15_minutely_temp
from utils.utils import get_next_timestamp

# Ignoring warnings
warnings.filterwarnings('ignore')

# Configuring logging
logging.basicConfig(level=logging.INFO)

# Constants
# Formatting parameters to get only the previous 15 minutes' temperature
WEATHER_PARAMS = {
    "latitude": 35.49,
    "longitude": -97.96,
    "temperature_unit": "fahrenheit",
    "minutely_15": ["temperature_2m",
                    "dew_point_2m"],
    "past_minutely_15": 1,
    "forecast_minutely_15": 0

}
NEWEST_WEATHER_DATA_PATH = "C:\\Users\\ryana\\PycharmProjects\\liberty_project\\assets\\data\\current_telemetry_data.csv"
ORIGINAL_WEATHER_DATA_PATH = "C:\\Users\\ryana\\PycharmProjects\\liberty_project\\assets\\data\\past_telemetry_data.csv"
MODEL_SAVE_PATH = "C:\\Users\\ryana\\PycharmProjects\\liberty_project\\assets\\models\\weather_model.json"
TEMP_UPPER_BOUND = 100
TEMP_LOWER_BOUND = 20


def job():
    """
        Scheduled job to retrieve weather data, train a model, and forecast temperature.

        This function performs the following operations in sequence:
        1. Retrieves new 15-minute temperature data from the weather API
        2. Trains an XGBoost regression model on the updated dataset
        3. Predicts the temperature for the next 15-minute interval
        4. Logs a warning if the predicted temperature falls outside defined thresholds
    """
    logging.info("Grabbing New Data...")
    # Running the function to get API data every 15 minutes
    new_temps = get_15_minutely_temp(params=WEATHER_PARAMS,
                                    original_data_path=ORIGINAL_WEATHER_DATA_PATH,
                                    newest_data_path=NEWEST_WEATHER_DATA_PATH)
    logging.info("Ran!")

    # fitting new model
    model = fit_xgb_regression_model(df_path=NEWEST_WEATHER_DATA_PATH,
                                     model_save_path=MODEL_SAVE_PATH)

    # Making prediction on next temperature in 15 minutes
    next_time = get_next_timestamp(new_temps['time'].iloc[0])

    print(new_temps)

    # Creating a dataframe to house features for prediction
    df_for_pred = pd.DataFrame()
    df_for_pred['hour'] = [next_time.hour]
    df_for_pred['month'] = [next_time.month]
    df_for_pred['previous_15_min_temp'] = new_temps['temperature_2m'].iloc[3]
    df_for_pred['previous_30_min_temp'] = new_temps['temperature_2m'].iloc[2]
    df_for_pred['previous_45_min_temp'] = new_temps['temperature_2m'].iloc[1]
    df_for_pred['previous_1_hour_temp'] = new_temps['temperature_2m'].iloc[0]
    df_for_pred['previous_15_min_dew_point'] = new_temps['dew_point_2m'].iloc[3]

    print(df_for_pred)

    # Getting predicted temp for next 15 minutes
    predicted_temp = model.predict(df_for_pred)[0]

    logging.info(f"Projection Time: {next_time}")
    logging.info(f"Projected Temperature (F): {predicted_temp}\n")

    # Issuing basic alert if temperature is greater than 100 or less than 20 (arbitrary bounds)
    if predicted_temp < TEMP_LOWER_BOUND or predicted_temp > TEMP_UPPER_BOUND:
        logging.warning(f"forecasted temperature ({round(predicted_temp, 2)}) exceeds or dips below the range "
                        f"({TEMP_LOWER_BOUND}, {TEMP_UPPER_BOUND}). Prepare accordingly!")


if __name__ == '__main__':
    while True:
        job()
        # Pause execution for 15 minutes, then run again
        sleep(60 * 15)
