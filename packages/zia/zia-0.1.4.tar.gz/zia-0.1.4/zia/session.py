import json
import logging
import time
import os
import re
import requests
from http.cookiejar import Cookie

import yaml


from .defaults import load_config, RequestError, SessionTimeoutError

PROFILE_FILENAME = os.path.join(os.environ['HOME'], '.zscaler', 'profile.yaml')
PROFILE = 'default'

COOKIE_FILENAME = os.path.join(os.environ['HOME'], '.zscaler', 'cookie.yaml')

# constant
URL = 'url'
USERNAME = 'username'
PASSWORD = 'password'
APIKEY = 'apikey'


class Session(object):
    API_VERSION = 'api/v1'
    USER_AGENT = 'zia api sdk'
    REQUEST_TIMEOUTS = (5, 25)

    def __init__(self, profile='default'):
        self.profile = profile
        self._profile = None
        self.get_profile(name=profile)
        self.url = self._profile[URL]
        if self.url[-1] == '/':
            raise RuntimeError('url {} must not be end with "/".'.format(url))
        self.username = self._profile[USERNAME]
        self.password = self._profile[PASSWORD]
        (self.timestamp, self.obfuscated_api_key) = self._obfuscate_api_key(
            self._profile[APIKEY])
        self.session = requests.Session()
        self.load_cookie()

    def get_profile(self, filename=PROFILE_FILENAME, name=PROFILE, reread=False):
        if self._profile is None or reread:
            try:
                with open(filename) as file:
                    self._profile = yaml.safe_load(file)[name]
            except FileNotFoundError:
                raise RuntimeError(
                    'Cannot find profile file: {}'.format(filename))
        return self._profile

    def load_cookie(self, filename=COOKIE_FILENAME, name=PROFILE, reread=False):
        if len(self.session.cookies) == 0 or reread:
            try:
                y = None
                with open(filename) as file:
                    y = yaml.safe_load(file)
                for d in y[name].values():
                    c = Cookie(
                        d['version'],
                        d['name'],
                        d['value'],
                        d['port'],
                        d['port_specified'],
                        d['domain'],
                        d['domain_specified'],
                        d['domain_initial_dot'],
                        d['path'],
                        d['path_specified'],
                        d['secure'],
                        d['expires'],
                        d['discard'],
                        d['comment'],
                        d['comment_url'],
                        d['_rest'],
                        d['rfc2109'])
                    if c.is_expired():
                        LOGGER.warning('cookie expired : {}'.format(d['name']))
                        continue
                    d['expires'] = None
                    self.session.cookies.set_cookie(c)
            except FileNotFoundError:
                LOGGER.warning('Cannot find cookie file: {}'.format(filename))
            except KeyError:
                LOGGER.warning(
                    'Cannot find cookie profile: {}'.format(filename))

    def save_cookie(self, filename=COOKIE_FILENAME, name=PROFILE):
        y = {}
        try:
            with open(filename) as file:
                y = yaml.safe_load(file)
        except FileNotFoundError:
            pass
        if name not in y:
            y[name] = {}
        for c in self.session.cookies:
            y[name][c.name] = c.__dict__
            if c.name == 'JSESSIONID' and 'expires' in y[name][c.name]:
                # override session cookie(d['expires']==None) for cli
                # expire_datetime = datetime.datetime.utcnow() + datetime.timedelta(seconds=2*60*60)
                # y[name][c.name]['expires'] = expire_datetime.strftime('%a, %d %b %Y %H:%m:%S GMT')
                # 2 hours is no basis.
                y[name][c.name]['expires'] = int(time.time()) + 2*60*60
        with open(filename, 'w') as file:
            yaml.dump(y, file)

    def _set_header(self, cookie=None):
        header = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': self.USER_AGENT
        }
        LOGGER.debug("HTTP Header: {}".format(header))
        return header

    def _obfuscate_api_key(self, api_key):
        now = str(int(time.time() * 1000))
        n = now[-6:]
        r = str(int(n) >> 1).zfill(6)
        key = ""
        for i in range(0, len(n), 1):
            key += api_key[int(n[i])]
        for j in range(0, len(r), 1):
            key += api_key[int(r[j])+2]
        LOGGER.debug(
            "OBFUSCATED APY KEY / Time: ***** / {}".format(now))
        return (now, key)

    def authenticate(self):
        path = 'authenticatedSession'
        try:
            if self.session.cookies.get('JSESSIONID'):
                LOGGER.info("cookie authentication")
                res = self.get(path)
                # GET /authenticatedSession does not validate session(JSESSIONID cookie), so execute other method
                self.get_status()
                LOGGER.info("authenticated")
                return res
        except SessionTimeoutError:
            LOGGER.info("session timedout. trying re-authn")
        LOGGER.info("password authentication")
        body = {
            'username': self.username,
            'password': self.password,
            'apiKey': self.obfuscated_api_key,
            'timestamp': self.timestamp
        }
        LOGGER.debug("HTTP BODY: {}".format(body))
        res = self.post(path, body)
        LOGGER.debug(res)
        if not res['authType']:
            raise RuntimeError('not authenticated')
        LOGGER.info('authenticated')
        self.save_cookie()

    def get_status(self):
        path = 'status'
        return self.get(path)

    def activate(self):
        path = 'status/activate'
        return self.post(path)

    def request(self, method, path, body=None):
        header = self._set_header()
        uri = "/".join([self.url, self.API_VERSION, path])
        LOGGER.debug('method {} path {} body {}'.format(
            method.__name__, path, body))
        kwargs = {
            'headers': header,
            'timeout': self.REQUEST_TIMEOUTS
        }
        if body:
            kwargs['json'] = body
        res_json = None
        error = None
        res = method(uri, **kwargs)
        code = {'code': res.text, 'message': res.text}
        try:
            res_json = res.json()
            error = res_json
        except json.decoder.JSONDecodeError:
            pass
        if res.ok:
            error = None
        if error and 'code' in error:
            raise RequestError(method.__name__, path, body, error)
        if error and re.match(r'Rate Limit', error['message']):
            # [API Rate Limit Summary | Zscaler](https://help.zscaler.com/zia/api-rate-limit-summary)
            # hint: ssl settings is very low limit(1/min and 4/hr)
            error['code'] = "REATELIMITEXCEEDED"
            error['message'] += ". Retry After {}".format(error['Retry-After'])
            raise RequestError(method.__name__, path, body, error)
        if res_json:
            return res_json
        if res.text == '[]':
            # /firewallFilteringRules returns [] as text?
            return []
        if len(res.text) == 0:
            return None
        if path == 'auditlogEntryReport/download':
            # csv download. text output is nothing wrong.
            pass
        elif re.search(r'<title>Zscaler Maintenance Page</title>', res.text):
            error = {'code': 'MAINTENANCE',
                     'message': 'undergoing maintenance'}
            raise RequestError(method.__name__, path, body, error)
        elif re.search(r'var contentString = "Something has gone wrong while attempting to display this page.";', res.text):
            error = {'code': 'ERROR', 'message': 'Something has gone wrong'}
            raise RequestError(method.__name__, path, body, error)
        elif res.text == 'SESSION_NOT_VALID':
            error = {'code': 'SESSION_NOT_VALID',
                     'message': 'maybe cookie timeout'}
            raise SessionTimeoutError(method.__name__, path, body, error)
        elif re.search(r'Request body is invalid', res.text):
            error = {'code': 'REQUEST_NOT_VALID', 'message': res.text}
            raise RequestError(method.__name__, path, body, error)
        else:
            LOGGER.warning("text output might be error: {}".format(res.text))
        # it may not be OK strictly becase api dit not return json.
        return res.text

    def get(self, path, body=None):
        return self.request(self.session.get, path, body)

    def post(self, path, body):
        return self.request(self.session.post, path, body)

    def put(self, path, body):
        return self.request(self.session.put, path, body)

    def delete(self, path):
        return self.request(self.session.delete, path)


LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    load_config()
    LOGGER.setLevel(logging.INFO)
    session = Session()
    LOGGER.info(session.authenticate())
    LOGGER.info(session.session.cookies.get('JSESSIONID'))
    LOGGER.info(session.authenticate())
