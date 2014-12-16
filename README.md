exim-gpg-filter
==============

Exim4 transport-filter to automatically
and transparently
encrypt outgoing emails
for all recipients

Install:
<pre>
cd /etc/exim4
git clone https://github.com/Interoberlin/exim-gpg-filter.git
</pre>

Open /etc/exim4/exim4.conf and append a transport_filter line to the remote_stmp section:
<pre>
remote_smtp:
  debug_print = "T: remote_smtp for $local_part@$domain"
  driver = smtp
  transport_filter = /etc/exim4/exim-gpg-filter/gpgfilter.py
</pre>

Fre software under the terms and conditions of the GNU Affero GPL v3.

Report wishes and bugs here:
https://github.com/Interoberlin/exim-gpg-filter/issues
