import time

VERBOSE = True


def getCurentTimeString():
    return time.strftime("%H:%M:%S", time.localtime())


def log(message):
    if VERBOSE:
        print("{message} -> {time}".format(message=message,
                                           time=getCurentTimeString()))
