# Third-party imports
import pandas as pd
import requests
import schedule
from schedule import repeat, every


# Constants
API_URL = "https://api.open-meteo.com/v1/forecast"


def get_15_minutely_temp(params,
                         original_data_path,
                         newest_data_path):
    # Making the request and capturing it's response
    # api url will not change, so not adding it as an optional arg
    response = requests.get(API_URL, params=params)
    new_data = pd.DataFrame(response.json()['minutely_15'])

    # Loading in telemetry data
    all_data = pd.read_csv(original_data_path)

    # Appending new data to end of all data
    all_data = pd.concat([all_data, new_data])

    all_data.to_csv(newest_data_path, index=False)

    return new_data



