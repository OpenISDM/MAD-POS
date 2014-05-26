#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, after_this_request, make_response, \
    render_template
import requests

app = Flask(__name__)


# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'rdf'])

# For a given file, return whether it's an allowed type or not


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

topic_url = ''


@app.route('/callback', methods=['POST'])
def callbackPost():
    print 'hello'
    f = request.files['image']
    print f
    f.save('./Resource/image-copy.jpg')
    d = request.files['rdf']
    print f
    d.save('./Resource/ex4-copy.rdf')

    return 'POST OK'


@app.route('/callback', methods=['GET'])
def callbackGet():
    query_string = request.args
    topic_url = query_string.get('hub.challenge')
    print topic_url
    if query_string.get('hub.mode') == 'denied':
        # print query_string.get('hub.mode')
        # print query_string.get('hub.topic')
        # print query_string.get('hub.reason')
        return 'Subscription Denied'
    elif query_string.get('hub.mode') == 'subscribe' or query_string.get('hub.mode') == 'unsubscribe':
        if topic_url == query_string.get('hub.challenge'):
            if 'hub.challenge' in query_string:
                return query_string.get('hub.challenge')
            else:
                return 'No value of hub.challenge'
        else:
            resp = make_response(render_template('Unknown.html'), 406)
            return resp
    else:
        resp = make_response(render_template('Unknown.html'), 406)
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
    app.run(host='0.0.0.0', port=int("8888"))
