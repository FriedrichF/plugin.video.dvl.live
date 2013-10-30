# coding: utf-8
'''
Created on 28.10.2013

@author: FriedrichF
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui
from HTMLParser import HTMLParser

#HTML Tags entfernen
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

def CATEGORIES():
        addDir('Aktuell','http://www.dvllive.tv',1,'')
        addDir('Männer','http://www.dvllive.tv/videos?tags%5Bliga%5D%5B%5D=Männer',2,'')
        addDir( 'Frauen','http://www.dvllive.tv/videos?tags%5Bliga%5D%5B%5D=Frauen',2,'')
        addDir( '2.Liga','http://www.dvllive.tv/videos?tags%5Bliga%5D%5B%5D=2.+Liga',2,'')
        addDates('LIVE Termine (Info)')
                       
def AKTUELL(url):
        #Links aus den neusten Videos auslesen
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #Finde Link und Titel
        matchLinkTitle=re.compile(r'<a href="(.+?)" title="(.+?)">').findall(link)
        
        #Finde Thumbnail adresse. Für großes Fenster anderer Ausdruck als kleine Fenster!
        matchThumb=re.compile(r'<img src="(.+?)" alt=".+?" width=".+?" height=".+?" />|<img alt=".+?" src="(.+?)" \/>').findall(link)
        for i in range(len(matchThumb)):
                req1 = urllib2.Request("http://www.dvllive.tv"+matchLinkTitle[i][0])
                req1.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response1 = urllib2.urlopen(req1)
                link1=response1.read()
                response1.close()
                match1=re.compile(r'data-version=".+?" href="(.+?)"').findall(link1)
                #Plot Finden
                matchPlot=re.compile(r'<h1>.+?</h1>(.+?)</div>', flags=re.MULTILINE|re.DOTALL).findall(link1)
                plot = strip_tags(matchPlot[0]).strip()
                
                if match1:
                    if matchThumb[i][0]=='':
                        thumb = matchThumb[i][1]
                    else:
                        thumb = matchThumb[i][0]
                    addLink(matchLinkTitle[i][1],match1[0],thumb,plot)
                
def VIDEOLINKS(url,name):
            #Links der Videoseiten aus der Übersicht auslesen
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile(r'<a href="(.+?)" title="(.+?)">(?:\n|\r\n?)                    <span class="thumb mini">(?:\n|\r\n?)                      <img alt=".+?" src="(.+?)" \/>').findall(link)
            
            #Link zu Video aus Videoseite auslesen
            for url,name,thumb in match:
                    url = "http://www.dvllive.tv"+url
                    req1 = urllib2.Request(url)
                    req1.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response1 = urllib2.urlopen(req1)
                    link1=response1.read()
                    response1.close()
                    match1=re.compile(r'data-version=".+?" href="(.+?)"').findall(link1)
                    #Plot Finden
                    matchPlot=re.compile(r'<h1>.+?</h1>(.+?)</div>', flags=re.MULTILINE|re.DOTALL).findall(link1)
                    plot = strip_tags(matchPlot[0]).strip()
                    #Wenn Link vorhanden Video Link hinzufügen
                    if match1:
                        addLink(name,match1[0],thumb,plot)
            
            #Überprüfen ob weitere Seiten vorhanden sind
            nextPage=re.compile(r'<a class="next_page" data-remote="true" rel="next" href="(.+?)">').findall(link)
            if len(nextPage) == 1:
                #nächste Seite in url Variable schreiben
                addDir("Nächste Seite","http://www.dvllive.tv"+nextPage[0],2,'')
        

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage,plot):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def addDates(name):
        req = urllib2.Request("http://www.dvllive.tv/live-termine")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #Finde LIVE Termine
        matchNext=re.compile(r'<h1>LIVE Termine</h1>.+?</p>(.+?)</div>', flags=re.MULTILINE|re.DOTALL).findall(link)
        
        nextDates = strip_tags(matchNext[0]).strip()
        
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png")
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": nextDates } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url='',listitem=liz,isFolder=False)
        return ok
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        AKTUELL(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
