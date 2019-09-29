from datetime import tzinfo
import pytz

timezone_name = "UTC"


def get_timezone() -> tzinfo:
    return pytz.timezone(timezone_name)
