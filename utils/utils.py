# Standard library imports
from datetime import timedelta

# Third-party imports
import pandas as pd




def get_next_timestamp(t):
    if isinstance(t, str):
        t = pd.to_datetime(t)
    return t + timedelta(minutes=15)