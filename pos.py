#!/usr/bin/python
# -*- coding: utf-8 -*-
""""
    Copyright (c) 2014  OpenISDM

    Project Name: 

        OpenISDM MAD

    Version:

        1.0

    File Name:

        pos.py

    Abstract:

        pos.py is a module of Interface Server (IS) of 
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
    render_template, url_for, redirect, abort, send_from_directory
import requests
import json
import sys
import os

app = Flask(__name__)

topic_url = ''

app.config['Cache_Folder'] = os.path.join(os.path.dirname(__file__), 'Cache')


# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(
    ['json', 'rdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET'])
def web_local_app():
    return render_template('index.html')


@app.route('/cache/<extension>')
def uploaded_file(extension):
    filename = 'Cache.' + extension
    return send_from_directory(app.config['Cache_Folder'], filename)


@app.route('/callback', methods=['POST'])
def callbackPost():
    f = request.files['file']
    if f and allowed_file(f.filename):
        extension = f.filename.rsplit('.', 1)[1]
        filename = 'Cache.' + extension
        save_path = os.path.join(app.config['Cache_Folder'] , filename)
        print save_path
        f.save(save_path)
        return 'PUSH Success'
    return 'PUSH file is not correct'


@app.route('/settopicurl', methods=['GET'])
def settopicurl():
    global topic_url
    topic_url = request.args.get('url')
    if topic_url != None:
        return 'Store Topic URL Success!'
    else:
        return 'Store Topic URL Failed!'


@app.route('/callback', methods=['GET'])
def callbackGet():
    query_string = request.args
    if query_string.get('hub.mode') == 'denied':
        resp = make_response(render_template('Accepted.html'), 202)
        return resp
    elif query_string.get('hub.mode') == 'subscribe' or query_string.get('hub.mode') == 'unsubscribe':
        if topic_url == query_string.get('hub.topic'):
            if 'hub.challenge' in query_string:
                return query_string.get('hub.challenge')
            else:
                return 'No value of hub.challenge, topic url is right'
        else:
            resp = make_response(render_template('Unknown.html'), 406)
            return resp
    else:
        resp = make_response(render_template('Unknown.html'), 406)
        return resp
