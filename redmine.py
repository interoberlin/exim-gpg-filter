#!/usr/bin/python

#from email import *

#
# Class for Redmine-specific Email parsing
#
class RedmineMail:
    #
    # Instantiate with reference to existing Email instance
    #
    # @param text: Email as array of lines without \n line ending
    #
    def __init__(self, lines):
        self.lines = lines

    #
    # Find the line, which separates the Redmine change summary from the attached Redmine ticket body
    #
    # @return: Line index of separator; counting starts with 0
    #
    def getSeparatorLineIndex(self):
        # check all lines
        for i in range(len(self.lines)):
            # line begins with separator string
            if self.lines[i].find('--------') == 0:
                return i

    #
    # Extract the first line of the Redmine ticket body
    #
    def getTicketBodyHeader(self):
        # ticket body immediately starts after separator line
        return self.lines[self.getSeparatorLineIndex()+1]

    #
    # Parse, to which Tracker the mail content is subject to
    #
    # @return: Tracker as string
    #
    def getTracker(self):
        # the string before the '#'
        return self.getTicketBodyHeader().split('#')[0].strip()
    
    #
    # Parse, to which Ticket number the mail content is subject to
    #
    # @return: Ticket number as string
    #
    def getTicketNumber(self):
        # the number after the '#'
        return self.getTicketBodyHeader().split('#')[1].split(':')[0]

#
# Unit-Test
#
# Run by executing this file: ./redmine.py
#
if __name__ == '__main__':
    lines = """Ziemlich aktualisiert
    
----------------------------------------
Poison Dart Frog #11293:
""".split('\n')
    mail = RedmineMail(lines)
    print "Tracker: "+mail.getTracker()
    print "Ticket: #"+mail.getTicketNumber()
