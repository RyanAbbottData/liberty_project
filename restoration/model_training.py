# Standard library imports
from datetime import datetime
import warnings

# Third-party imports
import requests
import schedule
from schedule import repeat, every, run_pending
import pandas as pd
import numpy as np
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_absolute_error