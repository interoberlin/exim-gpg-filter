#!/usr/bin/python

import sys
import gnupg

# message is piped to this script from stdin 
lines = sys.stdin.readlines()

# strip unencrypted Redmine headers
dont_show = ['X-Mailer: Redmine\n']
i = 0
while (i < len(lines)):
    try:
        dont_show.index( lines[i] )
        lines.remove( lines[i] )
        k -= 1
    except:
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

# encrypt content
gpg = gnupg.GPG()
recipients = ['mail@matthiasbock.net','florian.schwanz@interoberlin.de']
content = str(gpg.encrypt(content, recipients, always_trust=True))

# re-assemble headers and content
message = headers+'\n'+content

# output manipulated message
print message
