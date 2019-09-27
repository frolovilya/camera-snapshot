import sys
import datetime
import pytz

timezone_name = "UTC"


def get_timezone():
    return pytz.timezone(timezone_name)


def log(message, *args, out=sys.stdout):
    current_time = datetime.datetime.now(get_timezone()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(("[" + current_time + "] " + message).format(*args), file=out, flush=True)


def error(message, *args):
    log(message, *args, out=sys.stderr)
