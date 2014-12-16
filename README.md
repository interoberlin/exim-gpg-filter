gpg-mailfilter
==============

Exim4 transport-filter to automatically encrypt outgoing emails

<pre>
remote_smtp:
  debug_print = "T: remote_smtp for $local_part@$domain"
  driver = smtp
  transport_filter = /etc/exim4/exim-gpg-filter/gpgfilter.py
</pre>
