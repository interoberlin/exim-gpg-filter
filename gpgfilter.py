#!/usr/bin/python

import sys
import gnupg

# message is piped to this script from stdin 
lines = sys.stdin.readlines()

log = open('/var/log/exim4/mainlog','a')

# only filter emails from certain senders
mail = ''.join(lines)
if mail.find('redmine@interoberlin.de') == -1:
	print mail.strip()
	log.write('gpgfilter: not encrypting\n')
	exit(0)

log.write('gpgfilter: message encrypted\n')

# strip unencrypted Redmine headers
dont_show = ['X-Mailer: Redmine\n', 'X-Redmine-', 'Subject:']
i = 0
# for all lines:
while (i < len(lines)):
    removed = False
    for j in range(len(dont_show)):
        if lines[i].find(dont_show[j]) > -1:
            log.write('gpgfilter: Removed line "'+lines[i]+'"\n')
            lines.remove( lines[i] )
            removed = True
            break
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

headers += 'Subject: [Redmine]\n'

# encrypt content
gpg = gnupg.GPG()

# TODO: derive recipients from To,CC,BCC and Received:for headers
recipients = ['mail@matthiasbock.net','florian.schwanz@interoberlin.de','t.kuban@googlemail.com']

content = str(gpg.encrypt(content, recipients, always_trust=True))

# re-assemble headers and content
message = headers+'\n'+content

# output manipulated message
print message

log.close()
