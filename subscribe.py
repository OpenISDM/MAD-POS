#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import requests


def main(argv):
    pos_id = ''
    pos_type = 'fix'  # pos_type = fix or mobile default:fix
    is_url = 'http://140.109.22.197/hub/'
    try:
        opts, args = getopt.getopt(
            argv, "hP:U:Y:", ["posid=", "isurl=", "help", "postype="])
    except getopt.GetoptError:
        print 'subscribe.py  -P <pos_id> -U <is_url> -Y <pos_type>'
        sys.exit(2)
    if str(opts) == '[]':
        print 'You should add POS ID for subscribe, using opts -P or --pos_id '
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print 'subscribe.py  -P <pos_id> -U <is_url> -Y <pos_type>'
                sys.exit()
            elif opt in ("-P", "--posid"):
                pos_id = arg
            elif opt in ("-U", "--isurl"):
                is_url = arg
            elif opt in ("-Y", "--postype"):
                pos_type = arg
    print 'POS ID is "', pos_id
    print 'POS Type is "', pos_type
    print 'Interface Server URL is "', is_url
    discovery(pos_id, is_url, pos_type)


def discovery(pos_id, is_url, pos_type):
    payload = {
        'posId': pos_id,
        'posType': pos_type}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
        'Content-Type': 'text/plain; charset=utf-8',
        'Accept-Language': 'en-US,en;q=0.8'}
    r = requests.get(is_url, params=payload)
    print 'Hub URL', r.links['hub']['url']
    print 'Topic URL', r.links['self']['url']

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {
        'hub.mode': 'subscribe',
        'hub.topic': r.links['self']['url'],
        'hub.callback': 'http://subscriber.ngrok.com/callback'}

    r = requests.post(r.links['hub']['url'], data=payload, headers=headers)
    print r.text
    print r.headers

# print >> sys.stderr, 'sub.status_code %s' % r.status_code

if __name__ == "__main__":
    main(sys.argv[1:])
