#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, after_this_request, make_response, \
    render_template
import requests

app = Flask(__name__)


@app.route('/callback', methods=['POST'])
def callbackPost():
    f = request.files['file']
    print request.headers
    convert_filename_str = str(f)
    filename = convert_filename_str.rsplit("'",3)[1]
    f.save('./Cache/' + filename)
    return 'POST OK'


@app.route('/callback', methods=['GET'])
def callbackGet():
    query_string = request.args
    if query_string.get('hub.mode') == 'denied':
        resp = make_response(render_template('Accepted.html'), 202)
        return resp
    elif query_string.get('hub.mode') == 'subscribe' or query_string.get('hub.mode') == 'unsubscribe':
        if topic_url == query_string.get('hub.topic'):
            if 'hub.challenge' in query_string:
                print query_string.get('hub.challenge')
                return query_string.get('hub.challenge')
            else:
                print 'No value of hub.challenge, topic url is right'
                return 'No value of hub.challenge, topic url is right'
        else:
            resp = make_response(render_template('Unknown.html'), 406)
            print '406'
            return resp
    else:
        resp = make_response(render_template('Unknown.html'), 406)
        print '406'
        return resp


class startServer:

    def __init__(self, longlat, postype, isurl):
        print 'initialize.....'
        self.long_lat = longlat
        self.pos_type = postype
        self.is_url = isurl
        self.hub_url = ''
        self.topic_url = ''
        

    def discovery(self):
        print 'discovery.....'
        payload = {'longlat': self.long_lat, 'postype': self.pos_type}
        print payload
        print self.is_url
        r = requests.get(self.is_url, params=payload)
        print r.headers
        print 'Hub = %s' % r.links["hub"]["url"]
        print 'Topic = %s' % r.links["self"]["url"]
        self.hub_url = r.links["hub"]["url"]
        self.topic_url = r.links["self"]["url"]

    def subscribe(self):
        print 'subscirbe.....'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = {'hub.mode': 'subscribe', 'hub.topic': self.topic_url,
                   'hub.callback': 'http://140.109.22.153/callback'}
        url = self.hub_url
        print payload
        print url
        r = requests.post(url, data=payload, headers=headers)
        print 'sub.text %s' % r.text
        print 'sub.headers %s' % r.headers

if __name__ == '__main__':
    print 'Start Server.....'
    start = startServer('234023423,234234234', 'fixed', 'http://140.109.22.227/hub')
    start.discovery()
    start.subscribe()
    app.debug = True
    app.run(host='140.109.22.153', port=int("80"))
