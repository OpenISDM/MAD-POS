#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, after_this_request, make_response, \
    render_template
import requests

app = Flask(__name__)

topic_url = ''


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
        self.long_lat = longlat
        self.pos_type = postype
        self.is_url = isurl
        self.hub_url = ''
        self.topic_url = ''

    def discovery(self):
        payload = {'longlat': self.long_lat, 'postype': self.pos_type}
        r = requests.get(self.is_url, params=payload)
        print r.headers
        print 'Hub = %s' % r.links["hub"]["url"]
        print 'Topic = %s' % r.links["self"]["url"]
        self.hub_url = r.links["hub"]["url"]
        self.topic_url = r.links["self"]["url"]

    def subscribe(self):
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = {'hub.mode': 'subscribe', 'hub.topic': self.topic_url,
                   'hub.callback': 'http://localhost:8888/callback'}
        url = self.hub_url
        r = requests.post(url, data=payload, headers=headers)
        print 'sub.text %s' % r.text
        print 'sub.headers %s' % r.headers

if __name__ == '__main__':
    # start = startServer('234023423,234234234', 'fixed', 'http://localhost/hub')
    # start.discovery()
    # start.subscribe()
    app.debug = True
    app.run(host='0.0.0.0', port=int("888"))
