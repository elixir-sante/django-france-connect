# Import external libs
import random
import requests
from urllib.parse import urlencode

# Import Django stuff
from django.db import models
from django.conf import settings

class FranceConnectAuth(object):

    def __init__(
            self,
            url = 'https://fcp.integ01.dev-franceconnect.fr',
            eidas = 'eidas1',
            scope = 'openid identite_pivot email'):
        self.__url_authorize = settings.FRANCE_CONNECT_URL + '/api/v1/authorize'
        self.__url_logout = settings.FRANCE_CONNECT_URL + '/api/v1/logout'
        self.__url_token = settings.FRANCE_CONNECT_URL + '/api/v1/token'
        self.__url_userinfo = settings.FRANCE_CONNECT_URL + '/api/v1/userinfo'
        self.__url_callback = settings.FRANCE_CONNECT_CALLBACK_URL
        self.__url_callback_logout = settings.FRANCE_CONNECT_CALLBACK_DISCONNECT_URL
        self.__consistent_callback_params = '?' + 'elixir=rocks'
        self.__scope = scope
        self.__id = settings.FRANCE_CONNECT_CLIENT_ID
        self.__secret = settings.FRANCE_CONNECT_CLIENT_SECRET
        self.__eidas_level = eidas
        self.__token_access = None
        self.__token_id = None

    def authorize(self):
        """Generate France Connect OpenID authorization URL."""
        data = {
            'response_type': 'code',
            'client_id': self.__id,
            'redirect_uri': self.__url_callback + self.__consistent_callback_params,
            'scope': self.__scope,
            'acr_values': self.__eidas_level,
            'state': self.generate_nonce(16),
            'nonce': self.generate_nonce(16),
        }
        return self.__url_authorize + '?' + urlencode(data)

    def token(self, authorization_code):
        """Generate and request France Connect token."""
        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': self.__url_callback + self.__consistent_callback_params,
            'client_id':  self.__id,
            'client_secret': self.__secret,
            'code': authorization_code
        }
        r = requests.post(self.__url_token, data = data)
        if r.status_code is not 200:
            print(f'FranceConnectAuth > token: cannot get token from FranceConnect: {r.text}')
            return None
        r = r.json()
        self.__token_access = r['access_token']
        self.__token_id = r['id_token']
        return self.__token_id

    def userinfo(self, schema):
        """Get userinfo from France Connect."""
        if self.__token_access == None or self.__token_id == None:
            print('FranceConnectAuth > userinfo: need to get FC token before getting userinfo datas.')
            return None
        parameters = {'schema': schema}
        headers = {'Authorization': f'Bearer {self.__token_access}'}
        r = requests.get(self.__url_userinfo, params = parameters, headers = headers)
        return r.json()

    def logout(self, id_token = None):
        """Generate France Connect OpenID logout URL."""
        if not id_token and not self.__token_id:
            print(f'FranceConnectAuth > logout : you must provide id_token in args or in FranceConnectAuth object.')
        data = {
            'id_token_hint': id_token if id_token is not None else self.__token_id,
            'state': self.generate_nonce(16),
            'post_logout_redirect_uri': self.__url_callback_logout,
        }
        return self.__url_logout + '?' + urlencode(data)

    def generate_nonce(self, length = 8):
        """Generate pseudorandom number."""
        return ''.join([str(random.randint(0, 9)) for i in range(length)])
