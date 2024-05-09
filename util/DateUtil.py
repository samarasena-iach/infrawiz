from datetime import datetime


def convert_to_datetime(time_string):
    return datetime.strptime(time_string, "%Y-%m-%d, %H:%M:%S")