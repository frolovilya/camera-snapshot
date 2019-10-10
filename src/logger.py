import sys
import datetime
import multiprocessing as mp
import threading

import env

_logger_queue = mp.Manager().Queue()


def log(message, *args, is_error=False):
    current_time = datetime.datetime.now(env.get_timezone()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_message = ("[" + current_time + "] " + message).format(*args)
    try:
        _logger_queue.put((log_message, is_error))
    except Exception:
        _direct_print(log_message, is_error)


def error(message, *args):
    log(message, *args, is_error=True)


def _direct_print(message, is_error):
    print(message, file=sys.stdout if not is_error else sys.stderr, flush=True)


def start():
    def log_messages():
        try:
            for msg, is_error in iter(_logger_queue.get, str()):
                _direct_print(msg, is_error)
        except Exception:
            pass

    _logging_thread = threading.Thread(target=log_messages, daemon=True)
    _logging_thread.start()
