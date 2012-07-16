#!/usr/bin/env python

import sys
from lib.config import get_config
from lib.cache import get_cache, add_cache
from lib.torrent_tracking import series, new_episodes, download_torrent

def main():
    """Our main function that does all the work"""
    new_files = []
    c = get_config()

    ser = series()
    for s in ser:

        # load the correct module
        provider = 'Providers.%s' % s['provider']
        __import__(provider)
        episodes = sys.modules[provider].episodes

        print '\n'
        print 'Searching for episodes in %s using provider %s' % (s['name'], s['provider'])
        epis = episodes(s)

        new = new_episodes(epis, c['cachefile'], s['name'])

        for ep in new:

            # cgecj iyt data us wgat we expect
            if type(ep) != tuple:
                raise Exception('Your regular expression needs to pull a URL and unique episode number')

            print 'Found new episode!', ep

            # extract our ep_number and torrent url
            for e in ep:
                if  e.isdigit():
                    ep_number = e
                elif not e.isdigit():
                    torrent = e

            # add prefix if we have it configured
            try:
                tor = '%s%s' % (s['prefix'], torrent)
            except KeyError, e:
                tor = torrent

            # some sites tend to use ampersand urls
            tor = tor.replace('amp;', '')

            # download our torrent file
            file_name = '%s-%s%s' % (s['name'], ep_number, tor, c['download_path'])
            print 'Attempting to Download %s' % file_name
            download = download_torrent(s['name'], ep_number, tor, c['download_path'])
            print download

            add_cache(c['cachefile'], (torrent, s['name'] + ep_number))
            newfiles.append(file_name)

    # Notifications
    # send Email if enabled
    if new_files:
        if c['enable_email'] == 'True':
            from lib.email_notify import send_email
            send_email(
                    c['toaddr'],
                    c['fromaddr'],
                    new_files,
                    c['host'])

    # send SMS if enabled
    # requires pygooglevoice
    if new_files:
        if c['enable_sms'] == 'True':
            from lib.sms_notify import send_sms
            send_sms(
                    c['gmail_username'],
                    c['gmail_password'],
                    c['cellnumber'],
                    new_files)

# run main if we called directly
if '__main__' == __name__:
    main()
