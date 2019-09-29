import sys
import datetime

import env


def log(message, *args, out=sys.stdout):
    current_time = datetime.datetime.now(env.get_timezone()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(("[" + current_time + "] " + message).format(*args), file=out, flush=True)


def error(message, *args):
    log(message, *args, out=sys.stderr)
