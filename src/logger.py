import datetime


def log(message, *args):
    print(("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "] " + message).format(*args))
