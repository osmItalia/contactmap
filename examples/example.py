#! /usr/bin/env python
# *-* coding: utf-8 *-*
#
# Example of use of the contactmap library.
#
# This file and the example data file: grid.csv 
# are in the Public Domain (CC0 license)
#
# See <http://creativecommons.org/publicdomain/zero/1.0/> for details

import csv
import ConfigParser

from contactmap import names_within, MessageSender

INFILE = 'grid.csv'

with open(INFILE, 'r') as f:
    reader = csv.reader(f)
    # skip header
    reader.next()

    boxes = []
    for r in reader:
        minlon = float(r[1])
        minlat = float(r[3])
        maxlon = float(r[2])
        maxlat = float(r[4])
        boxes.append((minlon, minlat, maxlon, maxlat))


# send a sample message to yourself
config = ConfigParser.ConfigParser()
config.read('contactmap_example.cfg')

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

subject = u'Workshop a Rovereto "OSM Academy trentino"'
message = u'''
# Workshop "OSM Academy trentino: imparare a contribuire a OpenStreetMap"

Caro {username},

siamo un gruppo di mappatori trentini e volevamo segnalarti che stiamo
organizzando un workshop sull'utilizzo di OpenStreetMap. Ci saranno
delle presentazioni (di livello introduttivo) e faremo insieme un po'
di modifiche alla mappa.

Il Workshop si terrà a Rovereto dalle ore 18:00 alle ore 21:00, presso
l'Uban Center di Rovereto in Corso Rosmini 58
([mappa](http://www.openstreetmap.org/browse/node/2381015677) e
[sito](http://www.urbancenter.rovereto.tn.it/)).

Maggiori informazioni sono disponibili alla [pagina di
Rovereto](http://wiki.openstreetmap.org/wiki/Rovereto#Workshop) sul
wiki di OpenStreetMap.

Se hai domande puoi rispondere cliccando sul link in calce a questa
mail, iscriverti alla [mailing list
talk-it-trentino](https://lists.openstreetmap.org/listinfo/talk-it-trentino)
oppure contattarmi all'indirizzo consonni@fbk.eu

Speriamo sarai dei nostri.

Cristian (a.k.a. CristianCantoro)
ed i mapper della lista talk-it-trentino
'''

sent = set([])

for box in boxes:
    for name in names_within(*box):
        if name not in sent:
            sender.send_message(user=username,
                                subject=subject,
                                text=message.format(username=name)\
                                        .encode('utf-8')
                               )
            sent.add(name)
            print 'Send message to: {}'.format(name.encode('utf-8'))
        else:
            print 'Message already sent to: {}'.format(name)
