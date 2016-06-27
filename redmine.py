#!/usr/bin/python

from email import *

#
# Class for Redmine-specific Email parsing
#
class RedmineMail:
    #
    # Instantiate with reference to existing Email instance
    #
    def __init__(self, email):
        self.mail = email
    
    #
    # Parse, to which Tracker the mail content is subject to
    # returns String
    #
    def getTracker(self):
        return "Test"
    
    #
    # Parse, to which Ticket number the mail content is subject to
    # returns String
    #
    def getTicket(self):
        return "123"
