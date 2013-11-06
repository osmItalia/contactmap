#! /usr/bin/env python
# *-* coding: utf-8 *-*

import requests
import urllib
import ConfigParser

NEIS_BASEURL = 'http://resultmaps.neis-one.org/ooocs.php'


def names_in(minlon, minlat, maxlon, maxlat):
    params = {
        'ntype': 'activity',
        'bbox': '{minlon},{minlat},{maxlon},{maxlat}'.format(
            minlon=minlon,
            minlat=minlat,
            maxlon=maxlon,
            maxlat=maxlat
          )
    }

    res = requests.get(NEIS_BASEURL, params=params)

    if not res.ok:
        res.raise_for_status()

    features = res.json()['features']

    for f in features:
        yield f['properties']['n']

MAX_ZOOM_LATUNIT = 0.023481163
MAX_ZOOM_LONUNIT = 0.064373016


def grid(minlon, minlat, maxlon, maxlat):
    lon = minlon
    lat = minlat

    while lat < maxlat:
        while lon < maxlon:
            yield (lon, lat, lon + MAX_ZOOM_LONUNIT, lat + MAX_ZOOM_LATUNIT)
            lon = lon + MAX_ZOOM_LONUNIT
        lon = minlon
        lat = lat + MAX_ZOOM_LATUNIT


def names_within(minlon, minlat, maxlon, maxlat):
    for box in grid(minlon, minlat, maxlon, maxlat):
        for name in names_in(*box):
            yield name


class MessageSender(object):

    def __init__(self,
                 authenticity_token,
                 username,
                 location,
                 osm_session,
                 pk_id):
        self.authenticity_token = authenticity_token
        self.username = username
        self.location = location
        self.osm_session = osm_session
        self.pk_id = pk_id

    def send_message(self, user, subject, text):
        url = 'http://www.openstreetmap.org/message/new/{user}'.format(
                user=user
               )

        payload = {
            'utf8': urllib.unquote_plus('%E2%9C%93'),
            'authenticity_token': self.authenticity_token,
            'message[title]': urllib.unquote_plus(subject),
            'message[body]': urllib.unquote_plus(text),
            'commit': 'Send'
        }

        headers = {
            'Origin': 'http://www.openstreetmap.org',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Host': 'www.openstreetmap.org',
            'Accept-Language': 'it-IT,it;',
            'User-Agent': 'contactmap',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.openstreetmap.org/message/new/{username}',
            'Cookie': '_osm_username={username}; '
                      '_osm_location={location}; '
                      '_pk_ref.1.cf09=%5B%22%22%2C%22%22%2C1383685750%2C%22'
                      'http%3A%2F%2Fwiki.openstreetmap.org%2Fwiki%2F'
                      'OpenStreetMap_License%22%5D; '
                      '_osm_session={session}; '
                      '_pk_id.1.cf09={pk_id} '
                      '_pk_ses.1.cf09=*'.format(
                        username=self.username,
                        location=self.location,
                        session=self.osm_session,
                        pk_id=self.pk_id
                      ),
            'Connection': 'keep-alive'
        }

        requests.post(url, data=payload, headers=headers)

if __name__ == '__main__':

    # get a grid of boxes (minlon, minlat, maxlon, maxlat) in a given area
    # bounding box
    print
    print 'get grid points in (10.7, 45.8, 11.74, 45.84)'
    print
    i = 0
    for box in grid(10.7, 45.8, 11.74, 45.84):
        i = i + 1
        print i, box

    # get the name of the users in a given bounding box
    print
    for n in names_within(10.7, 45.8, 11.74, 45.84):
        print n

    # send a sample message to yourself
    config = ConfigParser.ConfigParser()
    config.read('example/contactmap.cfg')

    authenticity_token = config.get('authentication', 'authenticity_token')
    osm_session = config.get('cookie', 'osm_session')
    username = config.get('cookie', 'username')
    location = config.get('cookie', 'location')
    pk_id = config.get('cookie', 'pk_id')

    sender = MessageSender(authenticity_token=authenticity_token,
                           username=username,
                           location=location,
                           osm_session=osm_session,
                           pk_id=pk_id)

    print 'Send message to: {}'.format(username)

    message = """
    # Very long message
    This is a very long message, with:

    * markdown
    * a bullet list
    * other stuff

    There are also ordered lists:

    1. first point
    2. second point
    3. other points
    """

    sender.send_message(username, 'Test message', message)
