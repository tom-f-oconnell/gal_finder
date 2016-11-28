#!/usr/bin/env python

import pandas as pd

'''
# necessary?
import urllib2
import cookielib
import urllib
# don't have this one right now
#import requests
'''

# need to use python 2 because mechanize is not (yet?) supported in 3
import mechanize
from bs4 import BeautifulSoup
import re
import pickle

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

# look at typical contents of FlyLight expression string for acceptable anatomical regions
roi = 'ellipsoid body'
# uses the 'distribution' number (second in tuple) that Janelia lists for each region
# TODO max distribution instead? what does it mean? how diff from intensity?
# min_distribution = 2
min_intensity = 1

re_i = re.compile(roi + ' ' + '\(([0-9]),[0-9]\)')
re_d = re.compile(roi + ' ' + '\([0-9],([0-9])\)')
re_pairs = re.compile('\(([0-9]),[0-9]\)')
re_vnc = re.compile('\(([0-9])\)')

# elements of format (line, intensity_in_region, distribution_in_region, intensity_sum_out_of_region)
lines = []

for i in range(0,len(df)):
    nick = df.loc[i,:]['nickname']
    if type(nick) is str:
        janelia_id = df.loc[i,:]['nickname'][:6]
        print(janelia_id)

        br.open(url) 

        # the page actually only has one 'form'
        br.select_form(nr=0)

        # might want to use lines instead (just a string arg)
        try:
            br['line'] = [janelia_id]
        except mechanize._form.ItemNotFoundError:
            print('Line not found in FlyLight.')
            continue

        r = br.submit()
        data = r.read()

        soup = BeautifulSoup(data, 'lxml')

        # the contents of the table listing information about matching lines
        t = soup.find('table', id='linelist')

        expression = ''

        for i, c in enumerate(t.children):

            # i = 2 and i = 4 contain information about expression in different areas
            # central brain and vnc, respectively?
            # the latter is not always present
            if i == 2 or i == 4:

                tds = c.find_all('td')

                for j, t in enumerate(tds):

                    # should be the column with the expression data
                    if i == 2 and j == 4:
                        expression = t.contents[0]

                        intensity = int(re_i.search(expression).groups()[0])
                        distribution = int(re_d.search(expression).groups()[0])
                        expr_sum = sum([int(x) for x in re_pairs.findall(expression)]) - intensity

                        break

                    # TODO maybe dont add VNC intensity b/c many just havent been imaged
                    # maybe add mean for those that don't list this?

                    elif i == 4 and j == 4:

                        if len(t.contents) > 0:
                            expression = t.contents[0]
                            expr_sum = expr_sum + sum([int(x) for x in re_vnc.findall(expression)])

                        line = (janelia_id, intensity, distribution, expr_sum)
                        print(line)
                        lines.append(line)

                        break


# TODO take all over min intensity, sort ascending by external intensity
# sorted by intensity in roi (descending)
print(sorted(lines, key=lambda x: x[1], reverse=True))

# lines over min_intensity in roi, sorted (ascending) by intensity out of roi (including VNC)
print(sorted([l for l in lines if l[1] > min_intensity], key=lambda x: x[3]))

to_save = (roi, lines)
pickle.dump(to_save, open('roi_and_lines.p', 'wb'))
