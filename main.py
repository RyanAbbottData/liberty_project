"""
The main file of the project that will run the pipeline
"""
# Standard library imports
from datetime import timedelta
import warnings
import logging

# Third-party imports
import schedule
from schedule import repeat, every, run_pending
import pandas as pd
import numpy

# Project imports
from job.fit_xgb_regression_model import fit_xgb_regression_model
from job.get_15_minutely_temp_data import get_15_minutely_temp
from utils.utils import get_next_timestamp

# Ignoring warnings
warnings.filterwarnings('ignore')

# Constants
# Formatting parameters to get only the previous 15 minutes' temperature
WEATHER_PARAMS = {
    "latitude": 35.49,
    "longitude": -97.96,
    "temperature_unit": "fahrenheit",
    "minutely_15": "temperature_2m",
    "past_minutely_15": 1,
    "forecast_minutely_15": 0

}
NEWEST_WEATHER_DATA_PATH = "C:\\Users\\ryana\\PycharmProjects\\liberty_project\\assets\\data\\current_telemetry_data.csv"
ORIGINAL_WEATHER_DATA_PATH = "C:\\Users\\ryana\\PycharmProjects\\liberty_project\\assets\\data\\past_telemetry_data.csv"
MODEL_SAVE_PATH = "C:\\Users\\ryana\\PycharmProjects\\liberty_project\\assets\\models\\weather_model.json"
TEMP_UPPER_BOUND = 100
TEMP_LOWER_BOUND = 20


@repeat(every(15).minutes)
def job():
    print("Grabbing New Data...")
    # Running the function to get API data every 15 minutes
    new_temp = get_15_minutely_temp(params=WEATHER_PARAMS,
                         original_data_path=ORIGINAL_WEATHER_DATA_PATH,
                         newest_data_path=NEWEST_WEATHER_DATA_PATH)
    print("Ran!")

    # fitting new model
    model = fit_xgb_regression_model(df_path=NEWEST_WEATHER_DATA_PATH,
                                     model_save_path=MODEL_SAVE_PATH)

    # Making prediction on next temperature in 15 minutes
    next_time = get_next_timestamp(new_temp['time'].iloc[0])

    # features_for_pred = [get_next_timestamp(new_temp['time'].iloc[0]), new_temp['temperature_2m']]
    df_for_pred = pd.DataFrame()
    df_for_pred['hour'] = [next_time.hour]
    df_for_pred['month'] = [next_time.month]
    df_for_pred['previous_15_min_temp'] = new_temp['temperature_2m']

    predicted_temp = model.predict(df_for_pred)[0]

    assert type(predicted_temp) == numpy.float32

    if predicted_temp < TEMP_LOWER_BOUND or predicted_temp > TEMP_UPPER_BOUND:
        logging.warning(f"forecasted temperature ({round(predicted_temp, 2)}) exceeds or dips below the range "
                        f"({TEMP_LOWER_BOUND}, {TEMP_UPPER_BOUND}). Prepare accordingly!")


# Using Python's 'schedule' library to schedule a run every 15 minutes
schedule.every(15).minutes.do(get_15_minutely_temp)

if __name__ == '__main__':
    #while True:
    job()
        #run_pending()

