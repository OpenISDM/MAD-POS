#!/usr/bin/python
# -*- coding: utf-8 -*-
""""
    Copyright (c) 2014  OpenISDM

    Project Name: 

        OpenISDM MAD

    Version:

        1.0

    File Name:

        sub.py

    Abstract:

        sub.py is a module of Interface Server (IS) of 
        Mobile Assistance for Disasters (MAD) in the OpenISDM 
        Virtual Repository project.
        It handling the requests from Interface Server.

    Authors:  

        Johnson Su, johnsonsu@iis.sinica.edu.tw

    License:

        GPL 3.0 This file is subject to the terms and conditions defined 
        in file 'COPYING.txt', which is part of this source code package.

    Major Revision History:

        2014/6/3: complete version 1.0
        2014/6/4: complete version 1.1
        2014/6/6: complete version 1.2


"""

from flask import Flask, request, after_this_request, make_response, \
    render_template, url_for, redirect, abort, send_file
import requests
import json
import sys
import os

app = Flask(__name__)

topic_url = ''
resourcePath = os.path.abspath('./pythoncodes/mad_pos/Resource')

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(
    ['json', 'rdf', 'png', 'jpg', 'jpeg', 'gif'])


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
        filePath = resourcePath + '/Cache.rdf'
        if os.path.exists(filePath):
            return send_file(filePath, mimetype='application/rdf+xml', as_attachment=True, attachment_filename='dataFiles.rdf')
    elif topic_file == 'json':
        filePath = resourcePath + '/Cache.json'
        if os.path.exists(filePath):
            return send_file(filePath, mimetype='application/json', as_attachment=True, attachment_filename='dataFiles.json')
    elif topic_file == 'img':
        filePath = resourcePath + '/Cache.png'
        if os.path.exists(filePath):
            return send_file(filePath, mimetype='image/png', as_attachment=False, attachment_filename='imgMaps.png')
    else:
        return 'empty'


@app.route('/callback', methods=['POST'])
def callbackPost():
    f = request.files['file']
    if f and allowed_file(f.filename):
        extension = f.filename.rsplit('.', 1)[1]
        f.save(resourcePath + '/Cache.' + extension)
        return 'POST OK'
    return 'POST file is not correct'


@app.route('/settopicurl', methods=['GET'])
def settopicurl():
    global topic_url
    topic_url = request.args.get('url')
    print >> sys.stderr, '/settopicurl/topic_url'
    print >> sys.stderr, topic_url
    return 'good job! %s' % topic_url


@app.route('/callback', methods=['GET'])
def callbackGet():
    query_string = request.args
    print >> sys.stderr, query_string
    if query_string.get('hub.mode') == 'denied':
        resp = make_response(render_template('Accepted.html'), 202)
        return resp
    elif query_string.get('hub.mode') == 'subscribe' or query_string.get('hub.mode') == 'unsubscribe':
        print >> sys.stderr, 'topic_url'
        print >> sys.stderr, topic_url
        print >> sys.stderr, query_string.get('hub.topic')
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
        resp = make_response(render_template('Unknown.html'), 405)
        return resp
