#!/usr/bin/env python3

import pandas as pd
import urllib

# TODO manually remove stocks that are struck through on sheet
df = pd.read_csv('./dickinson_janelia_gals.csv')

url = 'http://flweb.janelia.org/cgi-bin/flew.cgi'
payload = '''Content-Type: multipart/form-data; boundary=---------------------------21080268983277907471363809946
Content-Length: 2570

-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="_search_toggle"

general
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="lines"


-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="line"

R64H11
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="genes"


-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="_gsearch"

Search
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="_search_logic"

AND
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="llines"


-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="_larval_search_logic"

AND
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="mlines"


-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="_disc_search_logic"

AND
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="dlines"


-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name="_embryo_search_logic"

AND
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

_search_toggle
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

dline
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

gene
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

mline
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

term
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

lline
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

gfp_pattern
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

line
-----------------------------21080268983277907471363809946
Content-Disposition: form-data; name=".cgifields"

lterm
-----------------------------21080268983277907471363809946--
'''

header = {'Host': 'flweb.janelia.org',
          'User-Agent': 
          'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
          'Accept':
          'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5',
          'Accept-Encoding': 'gzip, deflate',
          'Referer': 'http://flweb.janelia.org/cgi-bin/flew.cgi',
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '0',
          'Content-Type': 
          'multipart/form-data; boundary=---------------------------21080268983277907471363809946',
          'Content-Length': '2570'}
        
args = urllib.parse.urlencode({'line': 'R64H11'})

#urllib.request.Request(url, data=payload)
#d = urllib.urlopen(url, data=payload)
#d = urllib.urlopen(url, data=args.encode('ascii'))
#d = urllib.request.Request(url, data=args.encode('ascii'))
#d = urllib.request.urlopen(url, data=payload.encode('ascii'), headers=header)
r = urllib.request.Request(url, data=payload.encode('ascii'), headers=header)
with urllib.request.urlopen(r) as f:
    s = f.read()

'''
for i in range(0,len(df)):
    nick = df.loc[i,:]['nickname']
    if type(nick) is str:
        janelia_id = df.loc[i,:]['nickname'][:6]
        print(janelia_id)
'''
