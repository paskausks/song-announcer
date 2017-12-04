# coding=utf-8
import sys
import datetime

def logger(msg, err=False):
    """
    Very simple console logger
    """
    now = datetime.datetime.now()
    stream = sys.stderr if err else sys.stdout
    stream.write('[%s] %s\n' % (now.strftime('%H:%M'), msg))