# This is an additional provider for http://thepiratebay.org
# which supports searching

import urllib2
import re
from lib.config import get_config

def pirate_bay_search(series):
    """Search for a series on The Pirate Bay"""
    encode = urllib2.quote(series)
    url = 'http://thepiratebay.org/search/%s/0/99/200' % encode
    req = urllib2.urlopen(url)
    rss = req.read()

    match = re.compile('<a href="(.*)" class="detLink" title="Details for .*">(.*)</a>', re.IGNORECASE).findall(rss)
    return match

def episodes(s):
    """Search over the results of userRSS and extract episode numbers then return URLS
    for all episodes greater or equal to your star num"""
    epis = []
    items = pirate_bay_search(s['searchname'])
    for item in items:
        ep_num = re.search('%s\.S[0]?%sE([0]?\d*)', % (s['searchname'], s['season']), item[1], re.IGNORECASE)
        if ep_num:
            if int(ep_num.group(1)) >= int(s['startnum']):
                url = 'http://thepiratebay.org' + item[0]
                req = urllib2.urlopen(u)
                path = req.read()
                match = re.search('<a href="(.*\.torrent)" title="Download this torrent">Download this torrent</a>', page)
                if match:
                    epis.append((match.group[1]. ep_num.group(1)))

    return epis
