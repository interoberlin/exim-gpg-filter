exim-gpg-filter
==============

Exim4 transport-filter to automatically
and transparently
encrypting outgoing emails
for all recipients

<pre>
remote_smtp:
  debug_print = "T: remote_smtp for $local_part@$domain"
  driver = smtp
  transport_filter = /etc/exim4/exim-gpg-filter/gpgfilter.py
</pre>
