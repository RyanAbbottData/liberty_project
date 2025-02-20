# liberty_project

This notebook will demonstrate the work I have done for a data science project as part of the interview process for Liberty Oilfield Services <br>
<br>
The following are the objective and 5 guidelines to deliver on that objective: <br>
<br>

> Develop a machine learning pipeline that:
> 1. Ingests temperature telemetry data from an external API in real-time.
> 2. Performs exploratory data analysis to understand the data.
> 3. Builds a model to predict the temperature for the next 15 minutes.
> 4. Continuously evaluates and updates the model as new data becomes available.
> 5. Generates alerts when the predicted temperature exceeds a threshold.

## Structure

The following is the structure of this project:
```
liberty-project/
├── job/
│   ├── fit_xgb_regression_model.py    # Function to fit regression model to weather data
│   └── get_15_minutely_temp_data.py   # Gets most recent data from Open Meteo API and adds to current data
│
├── restoration/
│   |── model_training.py  # Code I used to fit and test original model
│   └── get_all_data.py    # Gets past temperature data in 15-minute increments going back 92 days
│
├── utils/
│   └── utils.py    # A file housing various utility functions
│
├── assets/
│   |── current_telemetry_data.csv  # CSV containing most recent data. Updated by get_15_minutely_data.py 
│   └── past_telemetry_data.csv  # CSV containing all past data. Created by get_all_data.py
│   
├── main.py   # Runs the job, meant to be executed in terminal.
├── liberty_project.ipynb   # Notebook where I originally started working on this project. It contains EDA and feature/hyperparameter testing.
└── README.md
```
**NOTE:** `assets` sub-directory is not on GitHub, as the data would take too much space.



  
