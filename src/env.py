import pytz

timezone_name = "UTC"


def get_timezone():
    return pytz.timezone(timezone_name)
