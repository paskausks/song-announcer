# coding=utf-8
from os import (path, stat)
import threading
from time import time
import BaseHTTPServer

from .log import logger
from . import (api, config)

__author__ = 'pundurs'


VERSION = '0.1'


class AlertServerException(Exception):
    """
    Exception raised from alert server errors
    """
    pass



class AlertRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Request handler for the local server
    """

    # Version string
    server_version = 'SpotifyAlertServer/%s' % VERSION

    # config.Config instance
    config = None


    def get_template_content(self, template='index.html', context={}):
        """
        Returns template contents as a string
        """
        with open(path.join(path.dirname(__file__), 'templates', template), 'r') as t:

            contents = t.read()

            for k in context.keys():
                contents = contents.replace('{{%s}}' % k, context[k])

            return contents


    def render(self, content, last_mod=time(), content_type='text/html', status=200):
        """
        Sends HTTP response headers and the contents of
        html_str or, if not provided, "index.html" as a response
        """
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Last-Modified', self.date_time_string(last_mod))
        self.send_header('Content-Length', len(content))
        self.end_headers()

        self.wfile.write(content)


    def render_current_song(self):
        """
        Sends HTTP response with the current playing song
        """
        songfile_path = self.config.get('songfile')
        with open(songfile_path) as f:
            self.render(f.read(), content_type='text/plain', last_mod=stat(songfile_path).st_mtime)



    def do_GET(self):
        """
        HTTP GET verb handler
        """
        if '/current-song' in self.path:
            # Current song requested by front-end
            self.render_current_song()
            return

        token_ttl = self.config.get_token_ttl()

        logger('Got request for widget. Time until next refresh: %ss' % token_ttl)

        self.render(self.get_template_content(context={
            # Context variables are used as "{{variable}}"
            'refresh': str(token_ttl * 1000), # Convert to ms,
            'token': self.config.token
        }))


    def log_message(format, *args):
        """
        Silence default server log handler.
        """
        pass


class AlertServer(object):
    """
    Main server class, which renders the "widget"
    """

    ADDR = '127.0.0.1'
    PORT = 15987


    def __init__(self):

        self.run = True

        # Check config
        try:
            self.cfg = config.Config()
        except config.ConfigException as e:
            raise AlertServerException(e.message)

        AlertRequestHandler.config = self.cfg

        # Clear token and get a new one
        self.cfg.clear_token()
        self._spotify_auth = api.SpotifyAuth(self.cfg)

        try:
            self._spotify_auth.set_token()
        except api.SpotifyAuthException as e:
            raise AlertServerException(e.message)

        # Set up automatic token refresh
        self._token_refresher = SpotifyTokenRefreshThread(self._spotify_auth, self.cfg)
        self._token_refresher.start()

        # Create server instance
        self._server = BaseHTTPServer.HTTPServer((self.ADDR, self.PORT), AlertRequestHandler)


    def serve_forever(self):
        """
        Sets up the server for listening.
        Blocking call.
        """
        self._server.serve_forever()


    def shut_down(self):
        """
        Cleanly shut down all processes
        """
        self._server.shutdown()
        self._token_refresher.stop()


class SpotifyTokenRefreshThread(threading.Thread):
    """
    Thread subclass for auto-refreshing the spotify oauth token
    """
    def __init__(self, spotify_auth, cfg):

        self._stop_event = threading.Event()
        self._spotify_auth = spotify_auth
        self._cfg = cfg
        self._shut_down = False

        super(SpotifyTokenRefreshThread, self).__init__(name='SpotifyTokenRefreshThread')

    def run(self):
        while not self._stop_event.is_set():
            self._stop_event.wait(self._cfg.token_lifetime - 60)
            if not self._shut_down:
                # Prevent refresh on shutdown
                logger('Refreshing Spotify OAuth token.')
                self._spotify_auth.set_token()

    def stop(self):
        self._shut_down = True
        self._stop_event.set()
