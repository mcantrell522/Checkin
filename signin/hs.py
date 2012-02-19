#!/usr/bin/python3
###############################################################################
# hs.py - Hokie Stalker
# Query the Virginia Tech people search service for information about a person.
# Licensed under the ISC License.
#
# https://github.com/mutantmonkey/hokiestalker
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
###############################################################################

import sys
import xml.etree.ElementTree as et
import xml.etree.cElementTree as et
#import lxml.etree as et
import urllib2 

__author__ = 'mutantmonkey <mutantmonkey@mutantmonkey.in>'
__license__ = 'ISC'

SEARCH_URL = "https://webapps.middleware.vt.edu/peoplesearch/PeopleSearch?"\
        "query={0}&dsml-version=2"
NS = '{urn:oasis:names:tc:DSML:2:0:core}'

rows = []


"""Return a formatted row for printing."""
def row(name, data):
    if data is None:
        return

    if type(data) == str:
        rows.append("{0:20s}{1}".format(name + ':', data))
    else:
        rows.append("{0:20s}{1}".format(name + ':', data[0]))

        # print additional lines if necessary, trimming off the first row
        if len(data) > 1:
            for line in data[1:]:
                rows.append("{0:20s}{1}".format('', line))

"""Parse the address from an LDAP response when $ is used to separate lines."""
def parse_addr(data):
    if data is None:
        return None
    addr = data.split('$')
    return addr

"""Check if the current attribute has the desired key."""
def is_attr(attr, key):
    return attr.attrib['name'] == key

"""Search LDAP using the argument as a query. Argument must be a valid LDAP
   query."""
def search(query):
    query = urllib2.quote(query)
    r = urllib2.Request(SEARCH_URL.format(query), headers={
        'User-agent': 'hokiestalker/2.0',
        })
    f = urllib2.urlopen(r)

    xml = et.parse(f)
    results = xml.findall('{0}searchResponse/{0}searchResultEntry'.format(NS))

    if len(results) <= 0:
        return []
    else:
        matches = []
    

    for entry in results:
        entry_data = {}
        for attr in entry:
            entry_data[attr.attrib['name']] = attr[0].text

        names = []
        if 'displayName' in entry_data:
            names.append(entry_data['displayName'])

        if 'givenName' in entry_data and 'sn' in entry_data:
            if 'middleName' in entry_data:
                names.append('{0} {1} {2}'.format(entry_data['givenName'],
                    entry_data['middleName'], entry_data['sn']))
            else:
                names.append('{0} {1}'.format(entry_data['givenName'],
                    entry_data['sn']))

        row('Name', names)

        if 'uid' in entry_data:
            row('UID', entry_data['uid'])

        if 'uupid' in entry_data:
            row('PID', entry_data['uupid'])

        if 'major' in entry_data:
            row('Major', entry_data['major'])
        elif 'department' in entry_data:
            row('Department', entry_data['department'])

        if 'title' in entry_data:
            row('Title', entry_data['title'])

        if 'postalAddress' in entry_data:
            row('Office', parse_addr(entry_data['postalAddress']))

        if 'mailStop' in entry_data:
            row('Mail Stop', entry_data['mailStop'])

        if 'telephoneNumber' in entry_data:
            row('Office Phone', entry_data['telephoneNumber'])

        if 'localPostalAddress' in entry_data:
            row('Mailing Address', parse_addr(
                entry_data['localPostalAddress']))

        if 'localPhone' in entry_data:
            row('Phone Number', entry_data['localPhone'])

        if 'mail' in entry_data:
            row('Email Address', entry_data['mail'])
        matches.append(entry_data)
        
    return matches

