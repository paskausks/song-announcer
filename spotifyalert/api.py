# coding=utf-8
from base64 import b64encode
from httplib import HTTPSConnection
import json
import urllib
from time import time

__author__ = 'pundurs'


class SpotifyAuthException(Exception):
    """
    Exceptions raised by SpotfifyAuth
    """
    pass



class SpotifyAuth(object):
    """
    Class to get token for Client Credentials Flow
    """
    def __init__(self, cfg):
        super(SpotifyAuth, self).__init__()
        self._cfg = cfg
        self.client_id = self._cfg.get('clientid')
        self.client_secret = self._cfg.get('clientsecret')

    def _get_http_headers(self):
        """
        Return HTTP headers needed for authentication to the Spotify Web API
        """
        return {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': 'Basic ' + b64encode('%s:%s' % (self.client_id, self.client_secret))
        }


    def set_token(self):
        """
        Get token from Spotify Accounts Service and update the configuration
        """
        params = urllib.urlencode({'grant_type': 'client_credentials'})
        conn = HTTPSConnection('accounts.spotify.com', timeout=5)
        conn.request('POST', '/api/token', params, self._get_http_headers())

        json_response = json.loads(conn.getresponse().read())

        if 'error' in json_response:
            raise SpotifyAuthException(
                'Spotify API returned: %s. Recheck your client ID in config.ini!' % json_response['error_description']
            )

        self._cfg.clear_token()
        self._cfg.token = json_response['access_token']
        self._cfg.token_lifetime = json_response['expires_in']
        self._cfg.token_last_refreshed = time()

        conn.close()
