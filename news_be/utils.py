from datetime import datetime

def is_within_n_hours(input_datetime, n_hours):
    """
    Check if the given datetime is within n_hours from now.

    :param input_datetime: The datetime to check, as a datetime.datetime object or a string in the format 'YYYY-MM-DD HH:MM:SS'.
    :param n_hours: Number of hours to check within, as an integer.
    :return: True if the datetime is within n_hours from now, False otherwise.
    """
    # Ensure input_datetime is a datetime.datetime object
    if isinstance(input_datetime, str):
        input_datetime = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")

    # Get the current datetime
    now = datetime.now()

    # Calculate the difference in seconds and convert to hours
    hour_difference = abs((input_datetime - now).total_seconds()) / 3600.0

    # Check if the difference is within n_hours
    return hour_difference <= n_hours
