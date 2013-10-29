# coding: utf-8
# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re


url = "http://www.dvllive.tv/frauen/dresdner-sc-vs-schweriner-sc-4"
req1 = urllib2.Request(url)
req1.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response1 = urllib2.urlopen(req1)
link1=response1.read()
response1.close()
match1=re.compile(r'data-version=".+?" href="(.+?)"').findall(link1)
#Video Link hinzufügen
if match1:
    print match1[0]
else:
    print "nicht"