import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,time,datetime



ADDON = xbmcaddon.Addon(id='plugin.video.lockedtv')
baseurl='http://www.bleb.org/tv/data/listings/0/'

    
def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link


    
def offset_time():
    offset = int(ADDON.getSetting('timefrom'))
    offset -= 12
    if offset == 0:
        return '0'

    sign = '+' if offset > 0 else ''

    return sign + str(offset)    
        
        
        
def offset_gmt():
    offset = int(ADDON.getSetting('gmtfrom'))
    offset -= 12
    if offset == 0:
        return '0'

    sign = '+' if offset > 0 else ''
    
    return sign + str(offset)    
        
    


def return_url(name):
    name=name.lower().replace(' ','')
    if 'skyaction' in name:
        url=baseurl+'sky_movies_action_thriller.xml'	
    elif 'skycomedy' in name:
        url=baseurl+'sky_movies_comedy.xml'	
    elif 'skydrama' in name:
        url=baseurl+'sky_movies_drama.xml'	
    elif 'skyfamily' in name:
        url=baseurl+'sky_movies_family.xml'	
    elif 'skygreats' in name:
        url=baseurl+'sky_movies_modern_greats.xml'	
    elif 'skypremier' in name:
        url=baseurl+'sky_movies_premiere.xml'	
    elif 'skysci-fi' in name:
        url=baseurl+'sky_movies_sci-fi_horror.xml'	
    elif 'skysports1' in name:
        url=baseurl+'sky_sports1.xml'	
    elif 'skysports2' in name:
        url=baseurl+'sky_sports2.xml'	
    elif 'skysports3' in name:
        url=baseurl+'sky_sports3.xml'	
    elif 'skysportsf1' in name:
        url=baseurl+'sky_sports_f1.xml'	
    elif 'skysportsnews' in name:
        url=baseurl+'sky_sports_news.xml'	
    elif 'skynews' in name:
        url=baseurl+'sky_news.xml'	
    elif 'bbcone' in name:
        url=baseurl+'bbc1.xml'
    elif 'bbctwo' in name:
        url=baseurl+'bbc2.xml'
    elif 'itv1' in name:
        url=baseurl+'p_itv1.xml'
    elif 'itv2' in name:
        url=baseurl+'p_itv2.xml'
    elif 'itv3' in name:
        url=baseurl+'p_itv3.xml'
    elif 'itv4' in name:
        url=baseurl+'p_itv4.xml'
    elif 'skyone' in name:
        url=baseurl+'sky_one.xml'
    elif 'channel4' in name:
        url=baseurl+'ch4.xml'
    elif 'skythriller' in name:
        url=baseurl+'sky_movies_crime_thriller.xml'
    elif 'jsc+' in name:
        url    =  'http://www.en.aljazeerasport.tv/fragment/aljazeera/fragments/components/ajax/channelList/channel/plus%s/maxRecords/0'%(name.split('+')[1])
    else:
        url=None
    return url

    


def tvguide(name):
    url=return_url(name)
    if 'Bein' in name:
	    For_Name=name
	    link   =  OPEN_URL(url).replace('\n','').replace('  ','')
	    link   =  link.split('<h')[1]
	    pattern='<td class="eventsCell hardAlign">(.+?)</td'
	    match = re.compile(pattern, re.M|re.DOTALL).findall(link)
	    return ' - '+match[0]
	        
    elif not 'None Found' in url:
    
        forOffset_gmt=offset_gmt()
        if '+' in forOffset_gmt:
        
            Z       =   forOffset_gmt.split('+')[1]
            t       =   datetime.datetime.today()- datetime.timedelta(hours = int(Z))
            t_hour  =   t - datetime.timedelta(hours = 1)
            
        elif '-' in forOffset_gmt:
        
            Z       =   forOffset_gmt.split('-')[1]
            t       =   datetime.datetime.today()+ datetime.timedelta(hours = int(Z))
            t_hour  =   t - datetime.timedelta(hours = 1)
             
        elif '-' in forOffset_gmt:
            t   =   datetime.datetime.today()+ datetime.timedelta(hours = int(Z))
            t_hour =   t - datetime.timedelta(hours = 1)
            
        else:
            t = datetime.datetime.today()
            t_hour =   datetime.datetime.today() - datetime.timedelta(hours = 1)
            
        link=OPEN_URL(url)
        link=link.split('<programme>')
        name ='<start>'+t.strftime('%H')
        _name ='<start>'+t_hour.strftime('%H')
        for p in link:
            if _name in p:
                match=re.compile('<title>(.+?)</title>').findall(p)
                return ' - '+match[0].replace('amp;','').strip()
            else:
                if name in p:
                    match=re.compile('<title>(.+?)</title>').findall(p)
                    return ' - '+match[0].replace('amp;','').strip()
    else:
        return ''

        

            
