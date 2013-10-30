# coding: utf-8
# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re
from HTMLParser import HTMLParser
from imaplib import Flags

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

url = "http://www.dvllive.tv/maenner/highlights-vfb-friedrichshafen-vs-generali-haching"
req1 = urllib2.Request(url)
req1.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response1 = urllib2.urlopen(req1)
link1=response1.read()
response1.close()
match1=re.compile(r'<h1>.+?</h1>(.+?)</div>', flags=re.MULTILINE|re.DOTALL).findall(link1)

plot = strip_tags(match1[0]).strip()

print plot