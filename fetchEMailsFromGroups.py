#!/usr/bin/python

# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import threading
import logging
import os
import datetime
import time
import sys
import pprint
import urllib
import urllib2
import httplib
import base64
import xml.sax
import xml.dom
from xml.dom import minidom
import StringIO
import fnmatch
#from urllib.parse import quote
import urlparse
import re

if len(sys.argv) != 3 :
	print "Usage: ./fetchEmailsFromGroups.py <fileContainingGroups> <outputFileName>"
	sys.exit(1)

groupList = str(sys.argv[1])
csvfile = str(sys.argv[2])

def getRequest(url):
	username = "jira_5_2_10"
	password="password"
        base64string = base64.encodestring('%s:%s' % (username,password)).replace('\n', '')
        base64string = base64.encodestring('%s:%s' % (username,password)).replace('\n', '')
        req = urllib2.Request(url, "", {'Content-Type': 'application/xml'})
        req.add_header("Authorization", "Basic %s" % base64string)
        req.get_method = lambda: 'GET'
        return req

def chunks(l,n):
        for i in range(0, len(l), n):
        	yield l[i:i+n]


def getEmail(content):
        xmldoc = minidom.parse(StringIO.StringIO(content))
        emailString=""
        for element in xmldoc.getElementsByTagName('user'):
		for isactive in element.getElementsByTagName('active'):
			if isactive.firstChild.data == "false":
				break
			else:
				for email in element.getElementsByTagName('email'):
					emailString = emailString + email.firstChild.data.encode("utf-8") + ";"
        return emailString


class SingletonType(type):
        _instances={}

        def __call__(cls, *args, **kwargs):
                if cls not in cls._instances:
                        cls._instances[cls]=super(SingletonType, cls).__call__(*args, **kwargs)
                return cls._instances[cls]

class MyLogger(object):
        __metaclass__ = SingletonType
        _logger=None

        def __init__(self):
                self._logger=logging.getLogger("crumbs")
                self._logger.setLevel(logging.DEBUG)
                formatter=logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')
                now=datetime.datetime.now()
                fileHandler=logging.FileHandler(now.strftime("%Y-%m-%d") + ".log")
                streamHandler=logging.StreamHandler()
                fileHandler.setFormatter(formatter)
                streamHandler.setFormatter(formatter)
                self._logger.addHandler(fileHandler)
                self._logger.addHandler(streamHandler)

        def get_logger(self):
                return self._logger

logger=MyLogger.__call__().get_logger()

emails = open(csvfile, "a")
f = open(groupList, 'rb')
for line in f:
       	crowdUrl = "https://crowd-3.dts.fm.rbsgrp.net/crowd/rest/usermanagement/latest/group/user/nested?groupname="+ line.rstrip(os.linesep)  + "&start-index=0&max-results=500&expand=user"
	print line.rstrip(os.linesep)
	try:
        	req=getRequest(crowdUrl)
		response = urllib2.urlopen(req)
	except urllib2.HTTPError:
        	print line.rstrip(os.linesep) + " not found"
        	continue
	data=response.read()
	emaillst = getEmail(data)
	emails.write(emaillst)
	emails.write("\n")
emails.close()
f.close()
