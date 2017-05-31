#!/usr/bin/python

class Email:
    def __init__(self, mail):

	# strip unencrypted Redmine headers
	dont_show = 0
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

    def isSender(self, address):
        return false    

    def splitHeadersFromContent(self):
        # separate headers from content
    for k in range(len(lines)):
        # the first empty line marks the end of header
        # and beginning of text sections
        if lines[k] == '' or lines[k] == '\n':
            break

    # array -> text
    headers = ''.join(lines[:k])
    content = ''.join(lines[k+1:])
