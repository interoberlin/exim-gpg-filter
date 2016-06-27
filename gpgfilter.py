#!/usr/bin/python

#
# This script is run by exim
# In Debian this scripts is run by user Debian-exim
#

import sys
import pprint
from subprocess import Popen,PIPE

from gpg2 import encrypt
from encoding import escape
from email import Email
from redmine import *
import config

log = open('/var/log/exim4/mainlog','a')

if debug:
    log.write('gpgfilter: running as user '+Popen(['whoami'],stdout=PIPE).communicate()[0])

#
# The message is piped to this script from stdin
# 
lines = sys.stdin.readlines()
mail = Email(lines)

# only filter emails from certain senders
if mail.isSender('redmine@interoberlin.de'):

    mail.stripHeaders( ['X-Mailer: ', 'X-Redmine-', 'Subject: ','List-Id: ', 'Content-Transfer-Encoding: '] )

	tracker = 'unknown'
	ticket = 'unknown'
	mail.setHeader("Subject", "[Redmine] "+tracker+" #"+ticket)
	mail.setHeader("Content-Transfer-Encoding", "8bit")

	# TODO: derive recipients from To,CC,BCC and Received:for headers
	# but it's also nice, to be able to decrypt forwarded/reply messages
	recipients = default_recipients
	content = encrypt(escape(mail.getContent()), recipients)

	if debug:
		log.write(content)
	else:
		log.write('gpgfilter: Message encrypted for '+','.join(recipients)+'\n')

	# output manipulated message
	print mail.getMessage()
	
elif mail.find('gitlab@interoberlin.de') != -1 :
    # strip unencrypted Gitlab headers
	dont_show = ['X-Mailer: ', 'Subject: ','List-Id: ']
	i = 0
	# for all lines:
	while (i < len(lines)):
		removed = False

		# for all field not to show:
		for j in range(len(dont_show)):
			# does current line contain the not to be shown field?
			if lines[i].find(dont_show[j]) > -1:
				# found: remove
				if debug:
					log.write('gpgfilter: removed line "'+lines[i].replace('\n','')+'"\n')
				lines.remove( lines[i] )
				removed = True
				
				# also cut following lines, if they belong to current line
				while (len(lines[i]) > 0 and lines[i][0] == ' '):
					if debug:
						log.write('gpgfilter: also removed line "'+lines[i].replace('\n','')+'"\n')
					lines.remove( lines[i] )
					
				break

		# if current line was removed, i already points to next line
		if not removed:
			i += 1

	# separate headers from content
	for k in range(len(lines)):
		# the first empty line marks the end of header
		# and beginning of text sections
		if lines[k] == '' or lines[k] == '\n':
			break

	# array -> text
	headers = ''.join(lines[:k])
	content = ''.join(lines[k+1:])

	headers += 'Subject: [Gitlab]\n'

	recipients = default_recipients
	content = encrypt(escape(content), recipients)
	
	if debug:
		log.write(content)
	else:
		log.write('gpgfilter: Message encrypted for '+','.join(recipients)+'\n')

	# re-assemble headers and content
	message = headers+'\n'+content

	# output manipulated message
	print message

else:
    print mail.strip()
    log.write('gpgfilter: not encrypting\n')
    exit(0)

log.close()
