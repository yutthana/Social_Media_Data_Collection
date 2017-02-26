# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 17:20:48 2016

@author: Yutthana
"""

import urllib2
from bs4 import BeautifulSoup
import csv
import socket
import httplib
import time


start = time.time()
timeout = 50
socket.setdefaulttimeout(timeout)


with open('firm_data_URL.csv', 'rb') as f, open('twitter_url.csv', 'wb') as w:
    cf = csv.reader(f)
    next(cf, None)
    writer = csv.writer(w)
    headers = ['twitter']  # returns the headers or `None` if the input is empty
    if headers:
        writer.writerow(headers)
        w.flush()
    for row in cf:
        if len(row[14]) > 0: #make sure the weburl is provided
            url = "http://" + row[14] #add http in front of url
            flag = 0 #if the file is written flag = 1, otherwise flag = 0 and write no twitter provided
            try: #check if the website is not forbidden, and timeout
                page = urllib2.urlopen(url, timeout=timeout)
            except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException) as e:
                flag = 1 #web cannot access
                writer.writerow(['Forbidden'])
                w.flush()
                continue
            except IOError:
                flag = 1 #web timed out
                writer.writerow(['socket timeout'])
                w.flush()
                continue
            except socket.timeout:
                flag = 1 #timed out
                writer.writerow(['socket timeout'])
                w.flush()
                continue
            
            soup = BeautifulSoup(page, 'lxml')
            

            for a in soup.find_all('a', href=True):
                try: #check if there is twitter link
                    if 'twitter.com' in a['href']:
                        flag = 1 #url found
                        twitterurl = a['href'].encode('utf8')
#                        url_list.append(twitterurl)
                        writer.writerow([twitterurl])
                        w.flush()
                        break
                except KeyError:
                    flag = 1 #no href
#                    twitterurl = 'no twitter provided'
#                    url_list.append('no twitter provided')
                    writer.writerow(['no facebook provided'])
                    w.flush()
                    break
  
        
            if flag == 0:
                writer.writerow(['no url'])
                w.flush()

        else:
            writer.writerow(['no url'])
            w.flush()

end = time.time()
print 'time used in min'
print (end - start)/60


