#!/usr/bin/env python

import pandas as pd

# necessary?
import urllib2
import cookielib
import urllib
# don't have this one right now
#import requests

# need to use python 2 because mechanize is not (yet?) supported in 3
import mechanize

from bs4 import BeautifulSoup

# TODO manually remove stocks that are struck through on sheet
df = pd.read_csv('./dickinson_janelia_gals.csv')

url = 'http://flweb.janelia.org/cgi-bin/flew.cgi'

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
        
#args = urllib.parse.urlencode({'line': 'R39A05'})

br = mechanize.Browser()

#br.set_all_readonly(False)
br.set_handle_robots(False)
br.set_handle_redirect(True)
br.set_handle_refresh(False)
br.set_handle_referer(True)
br.set_handle_gzip(True)


for i in range(0,len(df)):
    nick = df.loc[i,:]['nickname']
    if type(nick) is str:
        janelia_id = df.loc[i,:]['nickname'][:6]
        print(janelia_id)

        br.open(url) 

        # the page actually only has one 'form'
        br.select_form(nr=0)
        # might want to use lines instead (just a string arg)
        br['line'] = [janelia_id]
        r = br.submit()
        data = r.read()

        soup = BeautifulSoup(data, 'lxml')
        #print(soup.prettify())

        # the contents of the table listing information about matching lines
        t = soup.find('table', id='linelist')
        #print(t.prettify())

        break_all = False

        for i, c in enumerate(t.children):
            '''
            print(i, c)
            print('')
            print('')
            '''

            # i = 2 and i = 4 contain information about expression in different areas
            # central brain and vnc, respectively?
            # the latter is not always present
            if i == 2:
                #print(c.prettify())

                tds = c.find_all('td')

                for j, t in enumerate(tds):
                    '''
                    print(j, t)
                    print('')
                    print('')
                    '''

                    if j == 4:
                        print(t.contents)

                for j, g in enumerate(c.children):
                    #print(j, g)

                    # should be the column containing the expression information
                    if j == 5:
                        #print(g)

                        break_all = True
                        break

                if break_all:
                    break


