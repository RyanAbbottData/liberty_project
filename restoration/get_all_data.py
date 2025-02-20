# Third-party imports
import pandas as pd
import requests


# Defining parameters
# These are the points of longitude and latitude requested in the project instructions
# 'minutely_15' specifies that we want data points from every 15 minutes
# For this particular step I just want past, real data. Not forecast.
weather_params = {
    "latitude": 35.49,
    "longitude": -97.96,
    "temperature_unit": "fahrenheit",
    "minutely_15": "temperature_2m",
    "forecast_days": 0,
    "past_days": 92
}

# Making the request and capturing it's response
response = requests.get("https://api.open-meteo.com/v1/forecast", params=weather_params)

# Getting the data from the response
past_temp_data = response.json()['minutely_15']

# Converting JSON into a pandas dataframe
df = pd.DataFrame(past_temp_data)

# For some reason, some of the earliest data points are missing. I will remove them before writing the csv.
df_without_nans = df[df['temperature_2m'].notna()]

# Writing the CSV
df_without_nans.to_csv("../assets/data/past_telemetry_data.csv", index=False)
