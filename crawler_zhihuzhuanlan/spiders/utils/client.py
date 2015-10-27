import requests
import os
import json
from .common import *

class ZhihuClient:
    def __init__(self, cookies=None):
        self._session = requests.Session()
        self._session.headers.update(Default_Header)
        if cookies is not None:
            assert isinstance(cookies, str)
            self.login_with_cookies(cookies)

    def login_with_cookies(self, cookies):
        if os.path.isfile(cookies):
           with open(cookies) as f:
               cookies = f.read()
        cookies_dict = json.loads(cookies)
        self._session.cookies.update(cookies_dict)
