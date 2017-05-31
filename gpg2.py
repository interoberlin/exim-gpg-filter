#!/usr/bin/python

from subprocess import Popen,PIPE
from shlex import split

executable = "/usr/bin/gpg2"

def encrypt(plaintext, recipients):

    # TODO: remove recipients, for which the public key has expired
    
    cmd  = executable+" --no-verbose --quiet --trust-model always "
    r    = ['-r '+email for email in recipients]
    cmd += " ".join(r)
    cmd += " --yes --charset utf-8 --armor --output - -e"
    
    # prevent mail loss upon exception
    try:
        pgp_message = Popen(split(cmd), stdin=PIPE, stdout=PIPE).communicate(input=plaintext)[0]
    except:
        return plaintext

    lines = pgp_message.split('\n')
    lines.insert(1, 'Charset: UTF-8')
    cryptotext = '\n'.join(lines)
    
    return cryptotext

