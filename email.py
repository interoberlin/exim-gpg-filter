#!/usr/bin/python

#
# Class for Email parsing
#
class Email:
    #
    # Instantiate by splitting an array of lines into arrays of header and content lines
    #
    def __init__(self, mail):
        self.lines = mail
        self.headers = []
        self.content = []
        splitHeadersFromContent()

    #
    # Splits the lines of this message into header and content
    #        
    def splitHeadersFromContent(self):
        
        # Find the first empty line
        for k in range(len(self.lines)):
            # The first empty line marks the end of the header
            # and the beginning of text sections.
            if self.lines[k] == '' or self.lines[k] == '\n':
                break
        
        self.headers = lines[:k]
        self.content = lines[k+1:]


    # strip unencrypted Redmine headers
    dont_show = 
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
    
    #
    # Tests, whether the given address is the sender of this email
    # Checks the "From:" field
    #
    def isSender(self, address):
        return false    

    #
    # Returns the message headers as Array

    #
    # Returns the re-assembled message including headers and content
    #
    def getMessage(self):
        return headers+content
    
    #
    # Removes all occurences of any element in the listed headers
    # from this message's headers
    #
    def stripHeaders(self, headers):
        


