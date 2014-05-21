#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, after_this_request, make_response, \
    render_template
import requests

app = Flask(__name__)


@app.route('/callback', methods=['POST'])
def callback():
    return ''



if __name__ == '__main__':
    payload = {'longlat': '', 'postype': ''}
    r = requests.get('http://localhost/hub', params=payload)
    print r.headers
    print 'Hub = %s' % r.links["hub"]
    print 'Topic = %s' % r.links["self"]
    app.run(debug=True)
