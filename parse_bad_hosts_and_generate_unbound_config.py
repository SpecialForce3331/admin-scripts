#!/usr/bin/python

import urllib

f = urllib.urlopen("https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn-social/hosts")
out = open('/etc/unbound/local.d/blacklist.conf','w')

for line in f:
    if line.startswith('#') or line.startswith(' ') or line.startswith('\n') or line.startswith('\t'):
        continue
    splitted = line.split()
    host = splitted[1]
    result = 'local-zone: "{}" redirect\r\n'.format(host)
    result += 'local-data: "{} A 0.0.0.0"\r\n'.format(host)
    out.write(result)
