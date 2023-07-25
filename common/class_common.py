from datetime import datetime

from PyQt5 import QtWidgets


class Common:
    _instance = None

    # START_OF_HEADER = chr(1)
    START_OF_TEXT = chr(2)
    # END_OF_TEXT = chr(3)

    HOST = '127.0.0.1'
    PORT = 9999
    BUFFER = 50000
    FORMAT = "utf-8"
