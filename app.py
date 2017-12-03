# coding=utf-8
from spotifyalert import server
from spotifyalert.log import logger

__author__ = 'pundurs'


def run():

    try:
        httpd = server.AlertServer()
    except server.AlertServerException as e:
        logger(e.message, err=True)
        exit(1)

    logger('Access the widget at http://%s:%s.' % (server.AlertServer.ADDR, server.AlertServer.PORT))
    logger('Server running, press Ctrl+C to quit.')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger('Shutting down.')
        httpd.shut_down()
        exit(0)

if __name__ == '__main__':
    run()