"""
File to get the latest temperature data from Open Meteo
"""
# Third-party imports
import pandas as pd
import requests


# Constants
API_URL = "https://api.open-meteo.com/v1/forecast"


def get_15_minutely_temp(params,
                         original_data_path,
                         newest_data_path):
    """
        Retrieve 15-minute interval temperature data from an API, append it to existing data,
        and save the combined dataset.

        This function makes a request to the Open Meteo API endpoint using the provided parameters,
        extracts the 15-minute interval data from the response, appends it to existing historical
        data loaded from a file, and saves the combined dataset to a new file. It will also return the new data
        for use in main.py.

        Parameters
        ----------
        params : dict
            Dictionary of query parameters to send with the API request.
            These parameters configure the API call to retrieve the desired data.

        original_data_path : str
            Path to the CSV file containing existing historical temperature data.

        newest_data_path : str
            Path where the updated dataset (original + new data) will be saved.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing only the newly retrieved data from the API.
    """
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



