#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, after_this_request, make_response, \
    render_template, url_for, redirect, abort, send_file
import requests
import json
import sys
import os

app = Flask(__name__)

topic_url = 'http://140.109.22.227/topic'
resourcePath = os.path.abspath('./pythoncodes/mad_pos/Resource')

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['json', 'rdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/', methods=['GET'])
def root():
    print >> sys.stderr, "Start Server.....#1"
    return 'Server Check OK!!!!'

@app.route('/topic/<topic_file>', methods=['GET'])
def getTopic(topic_file):
    print >> sys.stderr, "getTopic with " + topic_file
    
    if topic_file == 'rdf':
        filePath = resourcePath + '/dataFiles.rdf'
        if os.path.exists(filePath):
            return send_file(filePath, mimetype='application/rdf+xml', as_attachment=True, attachment_filename='dataFiles.rdf')
    elif topic_file == 'json':
        filePath = resourcePath + '/dataFiles.json'
        if os.path.exists(filePath):
            return send_file(filePath, mimetype='application/json', as_attachment=True, attachment_filename='dataFiles.json')
    elif topic_file == 'img':
        filePath = resourcePath + '/imgMaps.png'
        if os.path.exists(filePath):
            return send_file(filePath, mimetype='image/png', as_attachment=False, attachment_filename='imgMaps.png')
    else:
      return 'empty'

@app.route('/callback', methods=['POST'])
def callbackPost():
    f = request.files['file']
    if f and allowed_file(f.filename):
        print >> sys.stderr, request.headers
        extension = f.filename.rsplit('.', 1)[1]
        if extension == 'rdf':
            fileanme = 'dataFiles.rdf'
        elif extension == 'json':
            filename = 'dataFiles.json'
        elif extension == 'png':
            filename = 'imgMaps.png'
        elif extension == 'jpg':
            filename = 'imgMaps.jpg'
        else:
            pass
        f.save(resourcePath + '/' + filename)
        return 'POST OK'
    return 'POST file is not correct'


@app.route('/callback', methods=['GET'])
def callbackGet():
    query_string = request.args
    print >> sys.stderr, query_string
    if query_string.get('hub.mode') == 'denied':
        resp = make_response(render_template('Accepted.html'), 202)
        return resp
    elif query_string.get('hub.mode') == 'subscribe' or query_string.get('hub.mode') == 'unsubscribe':
        if topic_url == query_string.get('hub.topic'):
            if 'hub.challenge' in query_string:
                print >> sys.stderr, query_string.get('hub.challenge')
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

        self.hub_url = r.links["hub"]["url"]
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
            'hub.callback': 'http://140.109.22.153/callback'}

        print >> sys.stderr, "payload..."
        print >> sys.stderr,  payload

        r = requests.post(self.hub_url, data=payload, headers=headers)

        print >> sys.stderr, 'sub.status_code %s' % r.status_code
        print >> sys.stderr, 'sub.text        %s' % r.text
        print >> sys.stderr, 'sub.headers     %s' % r.headers


if __name__ == '__main__':
    start = startServer(
        '234023423,234234234', 'fixed', 'http://140.109.22.227/hub')
    start.discovery()
    start.subscribe()
    app.debug = True
    app.run(host='140.109.22.153', port=int("80"), threaded=True)
