#!/usr/bin/python

#
# Diese Funktion ersetzt alle Vorkommnisse von Sonderzeichen
# durch naheliegende bzw. aehnliche ASCII-Ersetzungen
#
def escape(content):
    return content.replace("=C3=A4","ae").replace("=C3=BC","ue").replace("=C3=B6","oe").replace("=C3=84","Ae").replace("=C3=96","Oe").replace("=C3=9C","Ue").replace("=C3=9F","ss")
