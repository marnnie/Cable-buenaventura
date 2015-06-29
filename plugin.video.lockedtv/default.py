import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
from t0mm0.common.net import Net

import json


PLUGIN='plugin.video.lockedtv'
ADDON = xbmcaddon.Addon(id=PLUGIN)

image='http://www.xunitytalk.com/oss/'

auth=ADDON.getSetting('authtoken')


URL_SITE= 'http://'+ADDON.getSetting('site')+'.locked.tv'
BASEURL = URL_SITE+'/content/p/id/1/'

ERRORLOGO = xbmc.translatePath('special://home/addons/plugin.video.lockedtv/resources/art/redx.png')

THESITE='PROTV'

UA='XBMC'

net=Net()


                

def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link



datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, THESITE+'.lwp')
channeljs=os.path.join(cookie_path, "channel.js")
    
if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
    
    
def LOGGEDIN():
    USER = ADDON.getSetting('user')
    PASSWORD = ADDON.getSetting('password')
    if USER == '':
        xbmc.executebuiltin("XBMC.Notification([B][COLOR red]LockedTV Error[/COLOR][/B],Please Enter Username,7000,"+ERRORLOGO+")")
        keyboard = xbmc.Keyboard(USER, '[B]Please Enter Username[/B]'.title())
        keyboard.doModal()
        if keyboard.isConfirmed():
            USER = keyboard.getText()
            ADDON.setSetting(id='user', value=USER)

    if PASSWORD == '':
        xbmc.executebuiltin("XBMC.Notification([B][COLOR red]LockedTV Error[/COLOR][/B],Please Enter Password,7000,"+ERRORLOGO+")")
        keyboard = xbmc.Keyboard(PASSWORD, '[B]Please Enter Password[/B]'.title())
        keyboard.doModal()
        if keyboard.isConfirmed():
            PASSWORD = keyboard.getText()
            ADDON.setSetting(id='password', value=PASSWORD)

    url = URL_SITE+'/login/index'
    content = net.http_GET(url).content
    headers={'Accept':'*/*',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Accept-Language':'en-US,en;q=0.8',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':ADDON.getSetting('site')+'.locked.tv',
    'Origin':'http://'+ADDON.getSetting('site')+'.locked.tv',
    'Referer':'http://'+ADDON.getSetting('site')+'.locked.tv/login',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'}
    attempt=re.compile('name="login_attempt_id" value="(.+?)"').findall(content)[0]
    data={'amember_login':USER,'amember_pass':PASSWORD,'login_attempt_id':attempt}  
    html = net.http_POST(url,data, headers).content
    net.save_cookies(cookie_jar)
    r = re.findall(r'"ok":true', html)

    if r:
        return True
    else:
        return False
    

        
            
def GRAB_AUTH():
    print '###############     GRAB AUTH     #####################'
    net.set_cookies(cookie_jar)
    print BASEURL
    html = net.http_GET(BASEURL).content
    var  = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
    ADDON.setSetting('authtoken',var[0])
    now = datetime.datetime.today()
    ADDON.setSetting('login_time', str(now).split('.')[0])
    
    

    
def server():
    net.set_cookies(cookie_jar)
    return net.http_GET(URL_SITE+'/api/matrix/channels',headers={'User-Agent' :UA}).content
    
    
    
def CATEGORIES():
    if LOGGEDIN()==True:
        addDir('[COLOR gold].Upcoming Matches[/COLOR]','url',1999,'','','','')
        addDir('[COLOR green].New Movies[/COLOR]','http://pastebin.com/raw.php?i=S0td5yXK',6,'','','','')
        addDir('[COLOR cyan].HD Movies[/COLOR]','http://pastebin.com/raw.php?i=hwFSMzw9',6,'','','','')
        net.set_cookies(cookie_jar)

        link = json.loads(server())
        if ADDON.getSetting('genre')=='true':
            uniques=[]
            uniquesurl=[]
            data=link['categories']
            ret = ''
            for j in data:
                url = j
                name = data[j].encode("utf-8")       
                if name not in uniques:
                    uniques.append(name)
                    uniquesurl.append(url)
                    addDir(name,url,4,'','','','')
            

            
        else:
            data=link['channels']
            for field in data:
                id= str(field['id'])
                name= field['title'].encode("utf-8")            
                iconimage=image+name.replace(' ','').replace('-Free','').replace('HD','').replace('i/H','i-H').replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','').lower()+'.png'
                addDir(name,id,2,iconimage,'False','','')  

 
def Show_Dialog():
    dialog = xbmcgui.Dialog()
    dialog.ok("", '',"All Done Try Now", "")
        
def REPLAY():
        ok=True
        cmd = 'plugin://plugin.video.footballreplays/'
        xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)
        return ok
 
def GENRES(name,url):
    
    link = json.loads(server())
    data=link['channels']
    for field in data:
        id= field['id']
        title= field['title'].encode("utf-8")
        genre= field['cat_id']
        iconimage=image+title.replace(' ','').replace('HD','').replace('i/H','i-H').lower()+'.png'
        if url == genre:
            addDir(title,id,2,iconimage,'False','','')
                
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
        
    
 
    
def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

    


        
        
def PLAY_STREAM(name, url, iconimage, play, description):
    if play =='GET_EVENT':
        url=PLAY_FROM_EVENTS(name, url, iconimage, play, description)
        if not url:
            return Show_Cover()
    net.set_cookies(cookie_jar)
    stream_url= net.http_GET(URL_SITE+'/api/matrix/channel/%s'%url,headers={'User-Agent' :UA}).content
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url+' timeout=10')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz) 
        

def OnDemandLinks(url):

    link = OPEN_URL(url)
    if '<message>' in link:
       message=re.compile('<message>(.+?)</message>').findall (link)
       for name in message:
           addLink(name,'url','','')   

    LINKS=re.compile('<title>(.+?)</title.+?<link>(.+?)</link.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall (link)


    for name , url , iconimage in LINKS:
        addDir(name,url,7,iconimage,'','','','')



def afdah(url):
    url= 'https://m.afdah.org/watch?v='+url

    loginurl = 'https://m.afdah.org/video_info/html5'

    v=url.split('v=')[1]
    data={'v': v}
    headers = {'host': 'm.afdah.org','origin':'https://m.afdah.org', 'referer': url,
               'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'}

    first= net.http_POST(loginurl,data,headers).content

    link= json.loads(first)
    name=[]
    url=[]
    for j in link:
        name.append(j.upper())
   
        url.append('https://m.afdah.org'+link[j][3]) 

    THEURL= url[xbmcgui.Dialog().select('Please Select Resolution', name)]
    import requests
    r=requests.get(THEURL,allow_redirects=False)

    match=re.compile("(https\://redirector\.googlevideo.*?)'").findall(str(r.headers))[0]

    r = requests.get(match,allow_redirects=False)

    return r.headers['location']



def PlayOnDemand(url):
    import urlresolver

    if not 'googlevideo' in url:
        if not 'http' in url:
            url=afdah(url)
        else:    
            url=urlresolver.resolve(url)
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)   
    
def Show_Down():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), 'Sorry Channel is Down',"Will Be Back Up Soon", "Try Another Channel")  
    
def Show_Cover():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), '',"Sorry We Dont Cover This Channel", "")    

    
def PLAY_FROM_EVENTS(name, url, iconimage, play, description):
    name=name.split('[COLOR green]')[1].replace('[/COLOR]','')
    nameFINAL=[]
    urlFINAL=[]
    
    if ',' in name:
        nameSelect=[]
        urlSelect=[]
        name=name.split(',')
        for p in name:
            urlSelect.append(p.strip().lower())
            nameSelect.append(p.strip())
        TITLE = urlSelect[xbmcgui.Dialog().select('Please Select Channel', nameSelect)]      
        TITLE=TITLE.replace(' ','').lower().strip()
        link = server().split('{')
        print link
        for YOYO in link:
            if TITLE in YOYO.replace(' ','').lower():
                id = re.compile('"id":"(.+?)"').findall(YOYO)[0]
                NAME = re.compile('"title":"(.+?)"').findall(YOYO)[0]
                #GENRE = re.compile('"mediaid":"(.+?)"').findall(YOYO)[0]
                urlFINAL.append(id)
                nameFINAL.append('[COLOR green]%s[/COLOR]'%(NAME))
        if urlFINAL:
            return urlFINAL[xbmcgui.Dialog().select('Multiple Channels Found', nameFINAL)] 
        else:
            return False

                       
    else:
    
        NAME=name.replace(' ','').lower().strip()
        link = server().split('{')
        for YOYO in link:
                match = re.compile('"id":"(.+?)".+?"title":"(.+?)"').findall(YOYO)
                for id,NAME_ in match :

                    if NAME in NAME_.replace(' ','').lower().strip():
                        urlFINAL.append(id)
                        nameFINAL.append('[COLOR green]%s[/COLOR]'%(NAME_))
        if urlFINAL:
            return urlFINAL[xbmcgui.Dialog().select('Multiple Channels Found', nameFINAL)] 
        else:
            return False
            

def EVENTS():
    link = OPEN_URL('http://channelstatus.weebly.com/upcoming-events.html')
    link=link.split('<div class="paragraph" style="text-align:left;"')[1]
    link=link.split('>***')
    for p in link:
        try:
            DATE=re.compile('(.+?)\*').findall(p)[0]
            addDir('[COLOR cyan]'+DATE+'[/COLOR]','',2000,'','False','','')  
            match=re.compile('\[(.+?)\]</strong>__ (.+?) - (.+?)__',re.DOTALL).findall (p)
            for TIME ,VS , CHANNEL in match:

                CHANNEL=CHANNEL.replace('beIN','beIN Sports ').replace('Sports  Sports','Sports')
                name= '[COLOR white][%s][/COLOR][COLOR red]- %s -[/COLOR][COLOR green]%s[/COLOR]' %(TIME,VS,CHANNEL)
                addDir(name,'url',2,'','GET_EVENT','','')       
        except:pass
            
        
        
        
    
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

def addDir(name,url,mode,iconimage,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        #print name+'='+u
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Premiered":date,"Plot":description} )
        menu=[]
        liz.addContextMenuItems(items=menu, replaceItems=False)
        if mode == 2 or mode==7:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)    
        return ok



def addLink(name,url,iconimage, fanart):
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty("Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)

        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
date=None
description=None
page=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        play=urllib.unquote_plus(params["play"])
except:
        pass
try:
        date=urllib.unquote_plus(params["date"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        CATEGORIES()
               
elif mode==2:
        PLAY_STREAM(name,url,iconimage,play,description)

        
elif mode==4:
        GENRES(name,url)        
        
elif mode==3:
        REPLAY()

elif mode==5:
        OnDemand(url)


elif mode==6:
        OnDemandLinks(url)

elif mode==7:
        PlayOnDemand(url)         
        
elif mode==200:
        schedule(name,url,iconimage)
        
elif mode==201:
        fullguide(name,url,iconimage,description)
        
elif mode==202:
        LOGGEDIN()
        try:GRAB_AUTH()
        except:pass
        Show_Dialog()
        
elif mode==203:
        os.remove(cookie_jar)
        Show_Dialog()

elif mode==204:
        downloadchannel()      
        
elif mode==205:
        LOGOUT()   
        
elif mode==1999:
        EVENTS()        
        
elif mode==2001:
        ADDON.openSettings()

else:
        #just in case mode is invalid 
        CATEGORIES()

               
xbmcplugin.endOfDirectory(int(sys.argv[1]))

