import requests
import os
import json

class ZhihuClient:
    def __init__(self, cookies=None):
        Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                           'Referer': 'http://www.zhihu.com',
                           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                        'rv:39.0) Gecko/20100101 Firefox/39.0',
                           'Host': 'www.zhihu.com'}

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
