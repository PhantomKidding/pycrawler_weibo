import re
import urllib

import url_base62


def get_search_url(keyword, page=1):
    return 'http://s.weibo.com/weibo/' \
           + re.sub('_(%[^%]{2})%([^%]{2})_', r'\1\2',
                    urllib.quote(re.sub('(#|@)', r'_%\1_', keyword))) \
           + '&nodup=1&page=' + str(page)


def get_weibo_url(uid, mid):
    return 'http://www.weibo.com/' + str(uid) + '/' + url_base62.mid2Url(mid)
