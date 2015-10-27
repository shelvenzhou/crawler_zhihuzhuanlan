Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}

Zhihu_URL = 'http://www.zhihu.com'
Column_URL = 'http://zhuanlan.zhihu.com'
Column_API = Column_URL + '/api/columns'
Column_Data = Column_API + '/{0}'
Column_Posts_Data = Column_API + '/{0}/posts?limit=10&offset={1}'
UserColFollowed_URL = Zhihu_URL + '/people/{0}/columns/followed'