# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import urllib
import urlparse
from modules.libraries import cleantitle
from modules.libraries import client
from modules import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://www.movie25.ag'
        self.link_1 = 'http://www.movie25.ag'
        self.link_2 = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=http://www.movie25.ag'
        self.link_3 = 'https://movie25.unblocked.pw'
        self.search_link = '/search.php?key=%s'
        self.headers = {}


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                result = client.source(urlparse.urljoin(base_link, query), headers=self.headers)
                if 'movie_table' in str(result): break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "div", attrs = { "class": "movie_table" })

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "a", ret="title")[1]) for i in result]
            result = [i for i in result if any(x in i[1] for x in years)]

            result = [(client.replaceHTMLCodes(i[0]), i[1]) for i in result]
            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['u'][0], i[1]) for i in result]
            except: pass
            result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]

            match = [i[0] for i in result if title == cleantitle.movie(i[1])]

            match2 = [i[0] for i in result]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:10]:
                try:
                    if len(match) > 0:
                        url = match[0]
                        break
                    result = client.source(base_link + i, headers=self.headers)
                    if str('tt' + imdb) in str(result):
                        url = i
                        break
                except:
                    pass

            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                result = client.source(urlparse.urljoin(base_link, url), headers=self.headers)
                if 'link_name' in str(result): break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')

            quality = re.compile('>Links - Quality(.+?)<').findall(result)[0]
            quality = quality.strip()
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = client.parseDOM(result, "div", attrs = { "id": "links" })[0]
            links = client.parseDOM(links, "ul")

            for i in links:
                try:
                    host = client.parseDOM(i, "li", attrs = { "id": "link_name" })[-1]
                    try: host = client.parseDOM(host, "span", attrs = { "class": "google-src-text" })[0]
                    except: pass
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = client.parseDOM(i, "a", ret="href")[0]
                    url = client.replaceHTMLCodes(url)
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    if not url.startswith('http'): url = urlparse.urljoin(self.base_link, url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = urlparse.urlparse(url).path

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                result = client.request(urlparse.urljoin(base_link, url), headers=self.headers)
                if 'showvideo' in str(result): break

            result = result.decode('iso-8859-1').encode('utf-8')

            url = client.parseDOM(result, "div", attrs = { "id": "showvideo" })[0]
            url = url.replace('<IFRAME', '<iframe').replace(' SRC=', ' src=')
            url = client.parseDOM(url, "iframe", ret="src")[0]
            url = client.replaceHTMLCodes(url)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['url'][0]
            except: pass

            url = resolvers.request(url)
            return url
        except:
            return
