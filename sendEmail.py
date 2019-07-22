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
import string

if len(sys.argv) != 4 :
        print "Usage: ./sendEmail.py <emailHtmlTemplate> <fileContainingEMails> <EMailSubject>"
	print "Email List must be separated by colon. One line should contain not more than 300 emails"
        sys.exit(1)

content=sys.argv[1]
emailFile = str(sys.argv[2])
subject = str(sys.argv[3])

from_addr="FM-042651@rbos.co.uk"
to_addr="#DESToolsOperations@rbsres01.net"


f = open(content, "r")
html = f.read()
f.close()


def send_EMail(bcc_emails):
	#emails = bcc_emails + ";" + to_addr
	#print emails
	server = smtplib.SMTP('smtphost.fm.rbsgrp.net', 25)
	if __name__ == "__main__":
        	server.set_debuglevel(1)
	body_text = createMessage(html, bcc_emails)
	body = "From:"+from_addr+"To:"+to_addr+"BCC:"+bcc_emails+"Subject:"+subject
	emails=to_addr+bcc_emails
	server.sendmail(from_addr, bcc_emails.split(";"), body_text.as_string())
	server.quit()

def createMessage(html, bcc_addr):
        msg = MIMEMultipart('alternative')
	msgrel=MIMEMultipart('related')
	msg["Subject"]=subject
	msg["From"]=from_addr
	msg["To"]=to_addr
	msg["Bcc"]=bcc_addr
	msg.attach(msgrel)
	contemp=html
	matches=re.findall(r'\ssrc="([^"]+)"',contemp)
	matchcount=1
	for match in matches:
		html=re.sub(match,"cid:image"+str(matchcount),html)
		matchcount=matchcount+1
	part=MIMEText(html,'html')
	msgrel.attach(part)
	matchcount=1
	emailTemplateFolder = content.split('/')[0]
	for match in matches:
		imaddr=emailTemplateFolder+"/"+str(match)
		imagefile=open(imaddr,'rb').read()
		msgImg=MIMEImage(imagefile,'gif')
		msgImg.add_header('Content-ID',str('<image')+str(matchcount)+str('>'))
		msgImg.add_header('Content-Disposition','inline',filename=imaddr)
		msgrel.attach(msgImg)
		matchcount=matchcount+1
	#print(matches)
	#print(msg)
	return msg
	

f = open(emailFile, 'r')
try:
        for line in f:
                th = threading.Thread(target=send_EMail, args=(line, ))
                th.start()
		#time.sleep(30)
finally:
	f.close()


print("Done!")

