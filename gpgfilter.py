#!/usr/bin/python

#
# This script is run by exim
# In Debian this scripts is run by user Debian-exim
#

import sys
from gpg2 import encrypt
import pprint
from subprocess import Popen,PIPE
from redmine import RedmineMail

# message is piped to this script from stdin 
lines = sys.stdin.readlines()

log = open('/var/log/exim4/mainlog','a')

debug = False
if debug:
    log.write('gpgfilter: running as user '+Popen(['whoami'],stdout=PIPE).communicate()[0])

# only filter emails from certain senders
mail = ''.join(lines)

def escape(content):
    return content.replace("=C3=A4","ae").replace("=C3=BC","ue").replace("=C3=B6","oe").replace("=C3=84","Ae").replace("=C3=96","Oe").replace("=C3=9C","Ue").replace("=C3=9F","ss")

if mail.find('redmine@interoberlin.de') != -1 :
	# strip unencrypted Redmine headers
	dont_show = ['X-Mailer: ', 'X-Redmine-', 'Subject: ','List-Id: ', 'Content-Transfer-Encoding: ']
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

	rmail = RedmineMail(lines[k+1:])
	headers += "Subject: [Redmine] "+rmail.getTracker()+" #"+rmail.getTicketNumber()+"\n"
#	headers += "Subject: [Redmine]\n"
	headers += "Content-Transfer-Encoding: 8bit\n"

	# encrypt content
	#gpg = gnupg.GPG(gnupghome='/var/spool/exim4/.gnupg/', gpgbinary="/usr/bin/gpg2")
	#gpg.encoding = 'utf-8'

	# TODO: derive recipients from To,CC,BCC and Received:for headers
	# recipients = ["email@alice.org", "email@bob.org"]
	print message
	return

	#if debug:
	#	log.write('Available keys:\n'+pprint.pformat(gpg.list_keys())+'\n')
	#	log.write(content+'\n')

	#content = str(gpg.encrypt(content, recipients, always_trust=True))
	content = escape(content)
	content = encrypt(content, recipients)

	if debug:
		log.write(content)
	else:
		log.write('gpgfilter: Message encrypted for '+','.join(recipients)+'\n')

	# re-assemble headers and content
	message = headers+'\n'+content

	# output manipulated message
	print message
	
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

	# encrypt content
	gpg = gnupg.GPG(gnupghome='/var/spool/exim4/.gnupg/')

	# TODO: derive recipients from To,CC,BCC and Received:for headers
	# recipients = ["email@alice.org", "email@bob.org"]
	print message
	return
	
	if debug:
		log.write('Available keys:\n'+pprint.pformat(gpg.list_keys())+'\n')
		log.write(content+'\n')

	content = str(gpg.encrypt(content, recipients, always_trust=True))

	if debug:
		log.write(content)
	else:
		log.write('gpgfilter: message encrypted\n')

	# re-assemble headers and content
	message = headers+'\n'+content

	# output manipulated message
	print message

else:
    print mail.strip()
    log.write('gpgfilter: not encrypting\n')
    exit(0)

log.close()
