#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, after_this_request, make_response, \
    render_template, url_for, redirect, abort
import requests
import sys

app = Flask(__name__)

topic_url = 'http://140.109.22.181:8080/topic'


@app.route('/', methods=['GET'])
def root():
    print >> sys.stderr, "Start Server.....#1"
    return 'Server Check OK!!!!'


@app.route('/callback', methods=['POST'])
def callbackPost():
    f = request.files['file']
    print >> sys.stderr, request.headers
    convert_filename_str = str(f)
    filename = convert_filename_str.rsplit("'", 3)[1]
    f.save('./Cache/' + filename)
    return 'POST OK'


@app.route('/callback', methods=['GET'])
def callbackGet():
    query_string = request.args
    if query_string.get('hub.mode') == 'denied':
        resp = make_response(render_template('Accepted.html'), 202)
        return resp
    elif query_string.get('hub.mode') == 'subscribe' or query_string.get('hub.mode') == 'unsubscribe':
        app.logger.debug(topic_url)
        app.logger.debug(query_string.get('hub.topic'))
        if topic_url == query_string.get('hub.topic'):
            if 'hub.challenge' in query_string:
                app.logger.debug(query_string.get('hub.challenge'))
                return query_string.get('hub.challenge')
            else:
                print >> sys.stderr, 'No value of hub.challenge, topic url is right'
                return 'No value of hub.challenge, topic url is right'
        else:
            resp = make_response(render_template('Unknown.html'), 406)
            return resp
    else:
        resp = make_response(render_template('Unknown.html'), 406)
        return resp


class startServer:

    def __init__(self, longlat, postype, isurl):
        print >> sys.stderr, '...initialize...'
        self.long_lat = longlat
        self.pos_type = postype
        self.is_url = isurl
        self.hub_url = ''
        self.topic_url = ''

    def discovery(self):
        print >> sys.stderr, '...discovery...'

        payload = {
            'longlat': self.long_lat,
            'postype': self.pos_type}

        r = requests.get(self.is_url, params=payload)

        self.hub_url   = r.links["hub"]["url"]
        self.topic_url = r.links["self"]["url"]
        print >> sys.stderr,  'Hub = %s' % self.hub_url
        print >> sys.stderr,  'Topic = %s' % self.topic_url

    def subscribe(self):
        print >> sys.stderr, "...subscribe..."

        headers = {
            'content-type': 'application/x-www-form-urlencoded'}
        payload = {
            'hub.mode': 'subscribe',
            'hub.topic': self.topic_url,
            'hub.callback': 'http://140.109.22.181:8888/callback'}

        print >> sys.stderr, "payload..."
        print >> sys.stderr,  payload

        r = requests.post(self.hub_url, data=payload, headers=headers)

        print >> sys.stderr, 'sub.status_code %s' % r.status_code
        print >> sys.stderr, 'sub.text        %s' % r.text
        print >> sys.stderr, 'sub.headers     %s' % r.headers


if __name__ == '__main__':
    start = startServer(
        '234023423,234234234', 'fixed', 'http://140.109.22.181:8080/hub')
    start.discovery()
    start.subscribe()
    app.debug = True
    app.run(host='140.109.22.181', port=int("8888"), threaded=True)
