#!/usr/bin/env python

import os
import sys

if len(sys.argv) != 3 :
	print "Usage: ./remDuplicates.py <sourcefile> <targetfile>"
	print "Email List must be separated by semi-colon."
	sys.exit(1)

emailFile = str(sys.argv[1])
targetFile = str(sys.argv[2])

f = open(targetFile, 'a')
all_emails=[]
totCountB=0
totCountA=0
#emails=""
unique=[]
def chunks(l,n):
	for i in range(0, len(l), n):
		yield l[i:i+n]

with open(emailFile) as fp:
	for cnt, line in enumerate(fp):
		emails = line.split(";")
		all_emails.extend(emails)
	unique = list(dict.fromkeys(all_emails))
	all_emails = list(chunks(unique,1000))
	for i in range (len(all_emails)):
        	print len(all_emails[i])
		f.write(";".join(all_emails[i]))
		f.write("\n")

f.close()

