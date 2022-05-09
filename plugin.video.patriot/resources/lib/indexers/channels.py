# -*- coding: utf-8 -*-

'''
    Patriot Add-on

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
import sys
import random

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils


class channels:
    def __init__(self):
        self.base_link = 'https://ustvgo.tv'
        self.list = []

        self.categories = [
            {'title': 'All Channels', 'url': 'all_channels', 'image': '/wp-content/uploads/2020/09/cropped-icon_small-192x192.jpg'},
            {'title': 'News', 'url': '/category/news/', 'image': '/wp-content/uploads/2020/09/cropped-icon_small-192x192.jpg'},
            {'title': 'Sports', 'url': '/category/sports/', 'image': '/wp-content/uploads/2020/09/cropped-icon_small-192x192.jpg'},
            {'title': 'Kids', 'url': '/category/kids/', 'image': '/wp-content/uploads/2020/09/cropped-icon_small-192x192.jpg'},
            {'title': 'Entertainment', 'url': '/category/entertainment/', 'image': '/wp-content/uploads/2020/09/cropped-icon_small-192x192.jpg'}
            #{'title': 'Random Channel', 'url': 'random_channel', 'image': '/wp-content/uploads/2020/09/cropped-icon_small-192x192.jpg'}
        ]


        self.channels = [
            {'title': 'ABC', 'url': '/abc-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/abc-269x151.jpg'},
            {'title': 'ABC 7 New York', 'url': '/abc-7-new-york/', 'image': '/wp-content/uploads/2018/10/abc-269x151.jpg'},
            {'title': 'ACC Network', 'url': '/acc-network/', 'image': '/wp-content/uploads/2021/06/accn.jpg'},
            {'title': 'AE', 'url': '/ae-networks-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/AE.png'},
            {'title': 'AMC', 'url': '/amc-live/', 'image': '/wp-content/uploads/2019/01/AMC-1.png'},
            {'title': 'Animal Planet', 'url': '/animal-planet-live/', 'image': '/wp-content/uploads/2019/01/animal-planet.png'},
            {'title': 'BBCAmerica', 'url': '/bbc-america-live/', 'image': '/wp-content/uploads/2019/01/BBC.jpg'},
            {'title': 'BET', 'url': '/bet/', 'image': '/wp-content/uploads/2019/08/bet-269x151.png'},
            {'title': 'Big Ten Network', 'url': '/big-ten-network/', 'image': '/wp-content/uploads/2020/09/BTN.jpg'},
            {'title': 'Boomerang', 'url': '/boomerang/', 'image': '/wp-content/uploads/2019/08/Boomerang.png'},
            {'title': 'Bravo', 'url': '/bravo-channel-live-free/', 'image': '/wp-content/uploads/2019/01/bravo-269x151.png'},
            {'title': 'C-SPAN', 'url': '/c-span/', 'image': '/wp-content/uploads/2020/09/cspan-269x151-1.png'},
            {'title': 'Cartoon Network', 'url': '/cartoon-network/', 'image': '/wp-content/uploads/2019/01/cartoon-network.jpg'},
            {'title': 'CBS', 'url': '/cbs-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/CBS-1.png'},
            {'title': 'CBS 2 New York', 'url': '/cbs-2-new-york/', 'image': '/wp-content/uploads/2018/10/CBS-1.png'},
            {'title': 'CBS Sports Network', 'url': '/cbs-sports-network/', 'image': '/wp-content/uploads/2020/09/cbssn.jpg'},
            {'title': 'Cinemax', 'url': '/cinemax/', 'image': '/wp-content/uploads/2020/04/cinemax.jpg'},
            {'title': 'CMT', 'url': '/cmt/', 'image': '/wp-content/uploads/2019/08/cmt-1.png'},
            {'title': 'CNBC', 'url': '/cnbc-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/cnbc-1.jpg'},
            {'title': 'CNN', 'url': '/cnn-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/CNN-1.png'},
            {'title': 'Comedy Central', 'url': '/comedy-central-live-free/', 'image': '/wp-content/uploads/2019/01/comedy-central-269x151.png'},
            {'title': 'CW', 'url': '/the-cw-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/cw-269x151.png'},
            {'title': 'CW 11 New York', 'url': '/the-cw-11-new-york/', 'image': '/wp-content/uploads/2019/01/cw-269x151.png'},
            {'title': 'Destination America', 'url': '/destination-america/', 'image': '/wp-content/uploads/2019/08/Destination_America.png'},
            {'title': 'Discovery', 'url': '/discovery-channel-live/', 'image': '/wp-content/uploads/2019/01/Discovery.png'},
            {'title': 'Disney', 'url': '/disney-channel-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/disney-269x151.png'},
            {'title': 'DisneyJr', 'url': '/disneyjr/', 'image': '/wp-content/uploads/2019/08/disney-jr-768x432-1.png'},
            {'title': 'DisneyXD', 'url': '/disneyxd/', 'image': '/wp-content/uploads/2019/08/disney-xd-768x432-1.png'},
            {'title': 'Do it yourself (DIY)', 'url': '/diy/', 'image': '/wp-content/uploads/2019/08/diy.png'},
            {'title': 'E!', 'url': '/eonline/', 'image': '/wp-content/uploads/2019/08/E.png'},
            {'title': 'ESPN', 'url': '/espn-live/', 'image': '/wp-content/uploads/2019/01/espn-269x151.png'},
            {'title': 'ESPN2', 'url': '/espn2/', 'image': '/wp-content/uploads/2019/08/espn2-269x151.png'},
            {'title': 'ESPNews', 'url': '/espnews/', 'image': '/wp-content/uploads/2020/09/espnews-269x151-1.png'},
            {'title': 'ESPNU', 'url': '/espnu/', 'image': '/wp-content/uploads/2020/09/espnu-269x151-1.png'},
            {'title': 'FoodNetwork', 'url': '/food-network-live-free/', 'image': '/wp-content/uploads/2019/01/food-network-269x151.png'},
            {'title': 'FOX', 'url': '/fox-hd-live-streaming/', 'image': '/wp-content/uploads/2018/10/FOX-1.png'},
            {'title': 'FOX 5 New York', 'url': '/fox-5-new-york/', 'image': '/wp-content/uploads/2018/10/FOX-1.png'},
            {'title': 'Fox Sports 1 (FS1)', 'url': '/fox-sports-1/', 'image': '/wp-content/uploads/2019/01/fs1-269x151.png'},
            {'title': 'Fox Sports 2 (FS2)', 'url': '/fox-sports-2/', 'image': '/wp-content/uploads/2019/01/fs2-269x151.png'},
            {'title': 'FoxBusiness', 'url': '/fox-business-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/foxbusiness.jpg'},
            {'title': 'FoxNews', 'url': '/fox-news-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/foxnews.jpg'},
            {'title': 'Freeform', 'url': '/freeform-channel-live-free/', 'image': '/wp-content/uploads/2019/01/freeform-269x151.png'},
            {'title': 'FX', 'url': '/fx-channel-live/', 'image': '/wp-content/uploads/2019/01/fx-269x151.png'},
            {'title': 'FX Movie Channel', 'url': '/fxm/', 'image': '/wp-content/uploads/2019/08/FXM.png'},
            {'title': 'FXX', 'url': '/fxx/', 'image': '/wp-content/uploads/2019/08/FXX.png'},
            {'title': 'Game Show Network', 'url': '/gsn/', 'image': '/wp-content/uploads/2019/08/GSN.jpg'},
            {'title': 'Golf Channel', 'url': '/golf-channel-live-free/', 'image': '/wp-content/uploads/2019/01/golf-269x151.png'},
            {'title': 'Hallmark Channel', 'url': '/hallmark-channel-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/hallmark-chanel-logo.jpg'},
            {'title': 'Hallmark Movies and Mysteries', 'url': '/hallmark-movies-mysteries-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/HMM_logo_black-700x245.jpg'},
            {'title': 'HBO', 'url': '/hbo/', 'image': '/wp-content/uploads/2019/01/hbo-269x151.png'},
            {'title': 'HGTV', 'url': '/hgtv-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/HGTV-269x151.png'},
            {'title': 'History', 'url': '/history-channel-live/', 'image': '/wp-content/uploads/2019/01/History.png'},
            {'title': 'HLN', 'url': '/hln/', 'image': '/wp-content/uploads/2019/08/HLN.jpg'},
            {'title': 'Investigation Discovery', 'url': '/investigation-discovery-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/id-269x151.jpg'},
            {'title': 'ION (WPXN) New York', 'url': '/ion-wpxn-new-york/', 'image': '/wp-content/uploads/2020/09/cropped-icon_small-192x192.jpg'},
            {'title': 'Lifetime', 'url': '/lifetime-channel-live/', 'image': '/wp-content/uploads/2019/01/Lifetime-269x151.png'},
            {'title': 'Lifetime Movie Network', 'url': '/lifetime-movies/', 'image': '/wp-content/uploads/2019/08/lifetimeM.jpeg'},
            {'title': 'MLB Network', 'url': '/mlb-network/', 'image': '/wp-content/uploads/2019/05/MLB.png'},
            {'title': 'Motor Trend', 'url': '/motortrend/', 'image': '/wp-content/uploads/2019/08/Motortrend-1.png'},
            {'title': 'MSNBC', 'url': '/msnbc-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/msnbc_logo-269x151.jpg'},
            {'title': 'MTV', 'url': '/mtv/', 'image': '/wp-content/uploads/2019/08/mtv.jpg'},
            {'title': 'Nat Geo Wild', 'url': '/nat-geo-wild-live/', 'image': '/wp-content/uploads/2019/01/NatGeoWild.jpeg'},
            {'title': 'National Geographic', 'url': '/national-geographic-live/', 'image': '/wp-content/uploads/2019/01/National-Geographic-269x151.png'},
            {'title': 'NBA TV', 'url': '/nba-tv/', 'image': '/wp-content/uploads/2019/01/nbatv-269x151.jpg'},
            {'title': 'NBC', 'url': '/nbc/', 'image': '/wp-content/uploads/2018/10/nbc-logo.jpg'},
            {'title': 'NBC 4 New York', 'url': '/nbc-4-new-york/', 'image': '/wp-content/uploads/2018/10/nbc-logo.jpg'},
            {'title': 'NBC Sports (NBCSN)', 'url': '/nbc-sports/', 'image': '/wp-content/uploads/2019/01/nbcsn-269x151.jpg'},
            {'title': 'NFL Network', 'url': '/nfl-network-live-free/', 'image': '/wp-content/uploads/2019/01/nfln-logo-dark.png'},
            {'title': 'NFL RedZone', 'url': '/nfl-redzone/', 'image': '/wp-content/uploads/2020/09/NFLRZ.jpg'},
            {'title': 'Nickelodeon', 'url': '/nickelodeon-live-streaming-free/', 'image': '/wp-content/uploads/2019/01/Nickelodeon_2009.png'},
            {'title': 'Nicktoons', 'url': '/nicktoons/', 'image': '/wp-content/uploads/2019/08/nicktoons.png'},
            {'title': 'Olympic Channel', 'url': '/olympic-channel/', 'image': '/wp-content/uploads/2020/09/oly.jpg'},
            {'title': 'One America News Network', 'url': '/one-america-news-network/', 'image': '/wp-content/uploads/2019/09/OAN.jpg'},
            {'title': 'Oprah Winfrey Network (OWN)', 'url': '/own/', 'image': '/wp-content/uploads/2019/08/own.jpg'},
            {'title': 'Oxygen', 'url': '/oxygen/', 'image': '/wp-content/uploads/2019/08/Oxygen-1.png'},
            {'title': 'Paramount', 'url': '/paramount-network/', 'image': '/wp-content/uploads/2019/08/paramount.jpg'},
            {'title': 'PBS', 'url': '/pbs-live/', 'image': '/wp-content/uploads/2019/01/PBS.jpg'},
            {'title': 'POP', 'url': '/pop/', 'image': '/wp-content/uploads/2019/08/Pop_Network-1.png'},
            {'title': 'Science', 'url': '/science/', 'image': '/wp-content/uploads/2019/08/Science.jpg'},
            {'title': 'SEC Network', 'url': '/sec-network/', 'image': '/wp-content/uploads/2020/09/sec.jpg'},
            {'title': 'Showtime', 'url': '/showtime/', 'image': '/wp-content/uploads/2019/01/Showtime-269x151.png'},
            {'title': 'StarZ', 'url': '/starz-channel-live/', 'image': '/wp-content/uploads/2019/01/StarZ-269x151.png'},
            {'title': 'SundanceTV', 'url': '/sundance-tv/', 'image': '/wp-content/uploads/2019/08/sundance-tv.jpg'},
            {'title': 'SYFY', 'url': '/syfy-channel-live/', 'image': '/wp-content/uploads/2019/01/syfy-269x151.png'},
            {'title': 'TBS', 'url': '/tbs-channel-live-free/', 'image': '/wp-content/uploads/2019/01/tbs-269x151.png'},
            {'title': 'Telemundo', 'url': '/telemundo/', 'image': '/wp-content/uploads/2019/08/Telemundo.png'},
            {'title': 'Tennis Channel', 'url': '/tennis-channel-live-free/', 'image': '/wp-content/uploads/2019/01/TennisChannel.whiteBg.png'},
            {'title': 'The Weather Channel', 'url': '/the-weather-channel-live-streaming-free/', 'image': '/wp-content/uploads/2018/10/Weather-Channel-269x151.png'},
            {'title': 'TLC', 'url': '/tlc-live-free/', 'image': '/wp-content/uploads/2019/01/tlc-269x151.png'},
            {'title': 'TNT', 'url': '/tnt/', 'image': '/wp-content/uploads/2019/01/TNT.jpg'},
            {'title': 'Travel Channel', 'url': '/travel-channel-live-free/', 'image': '/wp-content/uploads/2019/01/Travel-269x151.png'},
            {'title': 'truTV', 'url': '/trutv/', 'image': '/wp-content/uploads/2019/08/TruTV-269x151.png'},
            {'title': 'Turner Classic Movies (TCM)', 'url': '/tcm/', 'image': '/wp-content/uploads/2019/05/TCM.png'},
            {'title': 'TV Land', 'url': '/tv-land-live-free/', 'image': '/wp-content/uploads/2019/01/TVLand-269x151.png'},
            {'title': 'Univision', 'url': '/univision/', 'image': '/wp-content/uploads/2019/08/univisionlogo.jpg'},
            {'title': 'USA Network', 'url': '/usa-network-live/', 'image': '/wp-content/uploads/2019/01/USA-Network-269x151.png'},
            {'title': 'VH1', 'url': '/vh1/', 'image': '/wp-content/uploads/2019/08/vh1.png'},
            {'title': 'We TV', 'url': '/we-tv/', 'image': '/wp-content/uploads/2019/08/wetv.jpg'},
            {'title': 'WWE Network', 'url': '/wwe-network/', 'image': '/wp-content/uploads/2019/09/wwe-269x151.png'},
            {'title': 'YES Network', 'url': '/yes-network/', 'image': '/wp-content/uploads/2020/04/yes.jpg'}
        ]


    def get(self):
        try:
            for i in self.categories:
                title = client.replaceHTMLCodes(i['title'])
                url = i['url']
                image = self.base_link + i['image']
                if i['url'] == 'random_channel':
                    action = 'channelsChannel'
                else:
                    action = 'channelsCategory'
                #self.list.append({'title': title, 'url': url, 'image': image, 'action': action})
                self.list.append({'title': title, 'url': url, 'image': 'DefaultVideoPlaylists.png', 'action': action})
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('get', 1)
            return self.list


    def scrapeCategory(self, url):
        try:
            if url == 'all_channels':
                for i in self.channels:
                    title = client.replaceHTMLCodes(i['title'])
                    link = self.base_link + i['url']
                    image = self.base_link + i['image']
                    self.list.append({'title': title, 'url': link, 'image': image, 'action': 'channelsChannel'})
            else:
                url = self.base_link + url
                html = client.scrapePage(url).text
                channels = client.parseDOM(html, 'div', attrs={'class': 'featured-image'})
                for i in channels:
                    title = client.parseDOM(i, 'a', ret='title')[0]
                    title = client.replaceHTMLCodes(title)
                    link = client.parseDOM(i, 'a', ret='href')[0]
                    image = client.parseDOM(i, 'img', ret='data-lazy-src')[0]
                    self.list.append({'title': title, 'url': link, 'image': image, 'action': 'channelsChannel'})
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('scrapeCategory', 1)
            return self.list


    def scrapeChannel(self, url):
        try:
            if url == 'random_channel':
                choice = random.choice(self.channels)
                url = self.base_link + choice['url']
            if not url.startswith('http'):
                url = self.base_link + url
            html = client.scrapePage(url).text
            try:
                title = client.parseDOM(html, 'meta', attrs={'property': 'og:title'}, ret='content')[0]
            except:
                title = url.replace(self.base_link, '')
            title = client.replaceHTMLCodes(title)
            link = client.parseDOM(html, 'iframe', ret='src')[0]
            if not link.startswith('http'):
                link = self.base_link + link
            html = client.scrapePage(link).text
            link = re.findall("var hls_src='(.+?)';", html)[0]
            item = control.item(path=link)
            item.setInfo(type='Video', infoLabels={'title': title})
            item.setProperty('IsPlayable', 'true')
            return control.player.play(link, item)
        except:
            log_utils.log('scrapeChannel', 1)
            return


def addDirectory(items, queue=False, isFolder=True):
    if items == None or len(items) == 0:
        control.idle()
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
    addonFanart = control.addonFanart()
    for i in items:
        try:
            url = '%s?action=%s&url=%s' % (sysaddon, i['action'], i['url'])
            title = i['title']
            thumb = i['image'] or 'DefaultVideo.png'
            item = control.item(label=title)
            item.setProperty('IsPlayable', 'true')
            item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
        except Exception:
            log_utils.log('addDirectory', 1)
            pass
    control.content(syshandle, 'addons')
    control.directory(syshandle, cacheToDisc=True)
