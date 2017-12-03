# coding=utf-8
import ConfigParser
from datetime import datetime
from os import path

__author__ = 'pundurs'

FILE = 'config.ini'
SECTION_SPOTIFY = 'spotify'
SECTION_TOKEN = 'api'


class ConfigException(Exception):
    """
    Exception raised on configuration errors
    """
    pass


class MisformattedConfigException(ConfigException):
    """
    Exception raised when an expected parameter in the config file wasn't found
    """
    def __init__(self, msg):
        super(MisformattedConfigException, self).__init__(
            'Misformatted configuration file! %s' % msg
        )


class Config(object):
    """docstring for Config"""

    def __init__(self):

        super(Config, self).__init__()

        # Path to config
        self._file = path.join(path.dirname(__file__), '..', FILE)

        # ConfigParser instance
        self._cfg = ConfigParser.RawConfigParser()
        parsed_cfg_files = self._cfg.read(self._file)

        if not parsed_cfg_files:
            raise ConfigException('Configuration could not be found! Please check if %s exists!' % FILE)

        # Check if current song file exists
        if not path.exists(self.get('songfile')):
            raise ConfigException('The current song file could not be found. Please check the value of "songfile" in config.ini and try again')



    def clear_token(self):
        """
        Clears the token and the token TTL from the config
        """
        self._cfg.remove_section(SECTION_TOKEN)
        self.write()



    @property
    def token(self):
        """
        Return Spotify Web API OAuth token
        """
        try:
            t = self.get('token', section=SECTION_TOKEN)
        except MisformattedConfigException:
            # Token doesn't exist
            return None

        return t


    @token.setter
    def token(self, t):
        """
        Store token in the config or deletes it, depending on the value of "t"
        """
        self._verify_token_section()
        self.set('token', t, section=SECTION_TOKEN)


    @property
    def token_lifetime(self):
        """
        Return time in seconds until token expires
        """
        try:
            ttl = self._cfg.getint(SECTION_TOKEN, 'tokenlifetime')
        except MisformattedConfigException:
            # Token TTL doesn't exist
            return 0

        return ttl


    @token_lifetime.setter
    def token_lifetime(self, ttl):
        """
        Store token TTL in the config
        """
        self._verify_token_section()
        self.set('tokenlifetime', ttl, section=SECTION_TOKEN)


    @property
    def token_last_refreshed(self):
        """
        Return time in seconds until token expires
        """
        try:
            ttl = self._cfg.getfloat(SECTION_TOKEN, 'lastrefresh')
        except MisformattedConfigException:
            # Token TTL doesn't exist
            return 0

        return ttl


    @token_last_refreshed.setter
    def token_last_refreshed(self, timestamp):
        """
        Store token TTL in the config
        """
        self._verify_token_section()
        self.set('lastrefresh', timestamp, section=SECTION_TOKEN)


    def get_token_ttl(self):
        """
        Return time left in seconds until token expires
        """
        return int(
            self.token_lifetime - (datetime.now() - datetime.fromtimestamp(self.token_last_refreshed)).total_seconds()
        )



    def get(self, param, section=SECTION_SPOTIFY):
        """
        Read a configuration parameter from the config
        """
        try:
            return self._cfg.get(section, param)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            raise MisformattedConfigException(e.message)



    def set(self, param, value, section=SECTION_SPOTIFY):
        """
        Set a parameter and write to the config file.
        """
        try:
            self._cfg.set(section, param, value)
        except ConfigParser.NoSectionError as e:
            raise MisformattedConfigException(e.message)

        self.write()


    def write(self):
        """
        Updates the configuration file with the new changes
        """
        with open(self._file, 'wb') as configfile:
            self._cfg.write(configfile)


    def _verify_token_section(self):
        """
        Checks if API section exists in config
        If not, creates it
        """
        if not self._cfg.has_section(SECTION_TOKEN):
            self._cfg.add_section(SECTION_TOKEN)
