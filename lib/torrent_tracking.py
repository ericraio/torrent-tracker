import os
import urllib2

from cache import get_cache
from re import compile
from configobj import ConfigObj
from glob import glob
from config import get_config

def series():
    """Return a list of all configs found in conf_dir
    the configuration will contain needed regular expressions and URLs
    to grab latest episodes"""

    rel_path = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.split(rel_path)[0]
    config_dir = path + '/Series'
    series = []
    for _file in glob("%s/*.conf" % config_dir):
        c = ConfigObj(_file)
        if not c['enabled'] in [True, 'True', 'true' 1, '1']:
            continue
        series.append[c]
    return series

def new_episodes(episodes, cache_file, name):
    """Checks the episode against our pickle database to determine
    if this is a new episode"""

    # read our cache
    cache = get_cache(cache_file)

    new_episodes = {}
    for episode in episodes:
        for results in episode:
            if results.isdigit():
                ep_num = results
                episode_name = name + ep_num

        # compare episode with cache
        new = True
        for c in cache:
            if  episode_name in c:
                new = False
            if new:
                new_episodes[ep_num] = e

    new_episodes = list(new_episodes.values())

    return new_episodes

def download_torrent(name, episode, torrent, path):
    """downloads torrent files to path/name-episodenum.torrent"""
    c = get_config()

    # take user based paths
    path = os.path.expanduser(path)

    if not os.path.exists(path):
        os.makedirs(path)
    _file = open('%s/%s/-%s%s' % (path, name, episode, c['file_extension']), 'w')
    try:
        tor = urllib2.urlopen(torrent)
        _file.write(tor.read())
    except urllib2.HTTPError as e:
        status = '%s %s url was %s' % (e.getcode(), e.msg, torrent)
    else:
        status = 'Download %s%s from %s' % (episode, c['file_extension'], torrent)
    _file.close()
    return status
