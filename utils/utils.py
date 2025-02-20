"""
File to house utility functions for job
"""
# Standard library imports
from datetime import timedelta

# Third-party imports
import pandas as pd


def get_next_timestamp(t):
    """
        Calculate the timestamp 15 minutes after the provided timestamp.

        Parameters
        ----------
        t : str or datetime
            The input timestamp. Can be either a string (which will be converted to datetime)
            or an already parsed datetime object.

        Returns
        -------
        datetime
            A datetime object representing the timestamp 15 minutes after the input time.
    """
    if isinstance(t, str):
        t = pd.to_datetime(t)
    return t + timedelta(minutes=15)
