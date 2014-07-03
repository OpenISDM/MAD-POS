#!/usr/bin/python
# -*- coding: utf-8 -*-
""""
    Copyright (c) 2014  OpenISDM

    Project Name: 

        OpenISDM MAD

    Version:

        1.0

    File Name:

        subscribe.py

    Abstract:

        PubHub.py is a module of Interface Server (IS) of 
        Mobile Assistance for Disasters (MAD) in the OpenISDM 
        Virtual Repository project.
        Subscribing to a topic URL consists of four parts 
        that may occur immediately in sequence or have a delay.

    Authors:  

        Johnson Su, johnsonsu@iis.sinica.edu.tw

    License:

        GPL 3.0 This file is subject to the terms and conditions defined 
        in file 'COPYING.txt', which is part of this source code package.

    Major Revision History:

        2014/6/3: complete version 1.0
        2014/6/10: complete version 1.1


"""

import sys
import getopt
import requests
import logging
import subprocess

logger = logging.getLogger('Subscribe')
logger.setLevel(logging.INFO)

# Produce formater first
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Setup Handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

# Setup Logger
logger.addHandler(console)
logger.setLevel(logging.INFO)

def set_up_ngrok(domain):
    '''
    ngrok lets you expose a locally running web service to the internet. 
    Just tell ngrok which port your web server is running on. 
    Let's try opening port 80 to the internet.
    '''
    import platform
    if platform.system() == 'Windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
        pid = subprocess.Popen([r"ngrok\ngrok.exe","-log=stdout","-authtoken", "W_0D4KY5as11SvSupBMT", "-subdomain=" + domain, str(80)], startupinfo=startupinfo).pid
    elif platform.system() == 'Linux':
        pid = subprocess.Popen(\
            ["nohup","./ngrok/ngrok","-log=stdout","-authtoken", "W_0D4KY5as11SvSupBMT", "-subdomain=" + domain, str(80)]).pid
    logger.info('Run in background process : ' + str(pid))

def get_opt(argv):
    '''
    Create a command program to get arg and opt.
    
     @param {String} [pos_id] POS ID for Interface Server
     @param {String} [pos_type] POS type for Interface Server
     @param {String} [is_url] Interface URL for HTTP requests
     @param {String} [subdomain] Callback domain for POS to set up callback URL
    '''
    pos_id = ''
    pos_type = 'fix'  
    is_url = 'http://140.109.17.57/hub/'

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
    logger.info('POS-ID : ' + pos_id)
    logger.info('POS-Type : ' + pos_type)
    logger.info('Interface Server URL : ' + is_url)

    # default Callback domain = subscribera
    # POS Callback URL : http://subscribera.ngrok.com
    set_up_ngrok(pos_id)

    # Call subscriber function
    subscribe(pos_id, is_url, pos_type)


def subscribe(pos_id, is_url, pos_type):
    '''
    '''

    # discovery
    payload = {
        'posId': pos_id,
        'posType': pos_type}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
        'Content-Type': 'text/plain; charset=utf-8',
        'Accept-Language': 'en-US,en;q=0.8'}
    r = requests.get(is_url, params=payload)
    
    logger.info('Hub URL : ' + r.links['hub']['url'])
    logger.info('Topic URL : ' + r.links['self']['url'])

    topic_url = r.links['self']['url']
    hub_url = r.links['hub']['url']

    # Storing topic URL
    payload = {
        'url': topic_url}
    r = requests.get('http://127.0.0.1/settopicurl', params=payload)
    logger.info('Results : ' + r.text)


    # Starting subscriber
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {
        'hub.mode': 'subscribe',
        'hub.topic': topic_url,
        'hub.callback': 'http://' + pos_id +'.ngrok.com/callback'}

    r = requests.post(hub_url, data=payload, headers=headers)
    logger.info('Interface Server Response Status Code : ' + str(r.status_code))
    logger.info('Interface Server Response Results : ' + r.content)

if __name__ == "__main__":
    get_opt(sys.argv[1:])
