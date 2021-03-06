################################################################################
#	  Copyright (C) 2015 Surfacingx										   #
#																			  #
#  This Program is free software; you can redistribute it and/or modify		#
#  it under the terms of the GNU General Public License as published by		#
#  the Free Software Foundation; either version 2, or (at your option)		 #
#  any later version.														  #
#																			  #
#  This Program is distributed in the hope that it will be useful,			 #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of			  #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the				#
#  GNU General Public License for more details.								#
#																			  #
#  You should have received a copy of the GNU General Public License		   #
#  along with XBMC; see the file COPYING.  If not, write to					#
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.	   #
#  http://www.gnu.org/copyleft/gpl.html										#
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
try:	from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from resources.libs import wizard as wiz

ADDON_ID	   = uservar.ADDON_ID
ADDONTITLE	 = uservar.ADDONTITLE
ADDON		  = wiz.addonId(ADDON_ID)
DIALOG		 = xbmcgui.Dialog()
HOME		   = xbmc.translatePath('special://home/')
ADDONS		 = os.path.join(HOME,	  'addons')
USERDATA	   = os.path.join(HOME,	  'userdata')
PLUGIN		 = os.path.join(ADDONS,	ADDON_ID)
PACKAGES	   = os.path.join(ADDONS,	'packages')
ADDONDATA	  = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADDOND		 = os.path.join(USERDATA,  'addon_data')
LOGINFOLD	  = os.path.join(ADDONDATA, 'Login')
ICON		   = os.path.join(PLUGIN,	'icon.png')
TODAY		  = date.today()
TOMORROW	   = TODAY + timedelta(days=1)
THREEDAYS	  = TODAY + timedelta(days=3)
KEEPLOGIN	  = wiz.getS('keeplogin')
LOGINSAVE	  = wiz.getS('loginlastsave')
COLOR1		 = uservar.COLOR1
COLOR2		 = uservar.COLOR2
ORDER		  = ['api-tmdb-htpctv', 'api-imdb-htpctv', 'api-fanart-tv-htpctv', 'api-tmdb-david', 'api-easynews-david', 'api-furk-david', 'api-tmdb-exegesis', 'api-imdb-exegesis', 'api-fanart-tv-exegesis', 'api-tmdb-patriot', 'api-imdb-patriot', 'api-fanart-tv-patriot', 'api-tmdb-scrubsv2', 'api-imdb-scrubsv2', 'api-fanart-tv-scrubsv2', 'api-tmdb-venom', 'api-imdb-venom', 'api-fanart-tv-venom', 'api-tmdb-judaea', 'api-tvdb-judaea', 'api-fanart-tv-judaea', 'api-tmdb-seren', 'api-tvdb-seren', 'api-fanart-tv-seren', 'api-tmdb-fen', 'api-easynews-fen', 'api-furk-fen', 'api-tmdb-exodusredux', 'api-imdb-exodusredux', 'api-fanart-tv-exodusredux', 'api-metaq', 'api-eis', 'api-opensubtitles', 'api-orion', 'api-metahandler', 'api-metadatautils']

LOGINID = {
	'api-tmdb-htpctv': {
		'name'	 : 'htpcTV - TMDb Personal API Key',
		'plugin'   : 'plugin.video.htpctv',
		'saved'	: 'api-tmdb-htpctv',
		'path'	 : os.path.join(ADDONS, 'plugin.video.htpctv'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.htpctv', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.htpctv', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-htpctv'),
		'settings' : os.path.join(ADDOND, 'plugin.video.htpctv', 'settings.xml'),
		'default'  : 'tm.user',
		'data'	 : ['tm.user'],
		'activate' : ''},
	'api-imdb-htpctv': {
		'name'	 : 'htpcTV - IMDb Personal API Key',
		'plugin'   : 'plugin.video.htpctv',
		'saved'	: 'api-imdb-htpctv',
		'path'	 : os.path.join(ADDONS, 'plugin.video.htpctv'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.htpctv', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.htpctv', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-imdb-htpctv'),
		'settings' : os.path.join(ADDOND, 'plugin.video.htpctv', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'	 : ['imdb.user'],
		'activate' : ''},
	'api-fanart-tv-htpctv': {
		'name'	 : 'htpcTV - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.htpctv',
		'saved'	: 'api-fanart-tv-htpctv',
		'path'	 : os.path.join(ADDONS, 'plugin.video.htpctv'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.htpctv', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.htpctv', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-fanart-tv-htpctv'),
		'settings' : os.path.join(ADDOND, 'plugin.video.htpctv', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'	 : ['fanart.tv.user'],
		'activate' : ''},
	'api-tmdb-david': {
		'name'	 : 'David - TMDb Personal API Key',
		'plugin'   : 'plugin.video.david',
		'saved'	: 'api-tmdb-david',
		'path'	 : os.path.join(ADDONS, 'plugin.video.david'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.david', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.david', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-david'),
		'settings' : os.path.join(ADDOND, 'plugin.video.david', 'settings.xml'),
		'default'  : 'tmdb_api',
		'data'	 : ['tmdb_api'],
		'activate' : ''},
    'api-easynews-david': {
        'name'     : 'EasyNews - David',
        'saved'    : 'api-easynews-david',
        'plugin'   : 'plugin.video.david',
		'path'	 : os.path.join(ADDONS, 'plugin.video.david'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.david', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.david', 'fanart.jpg'),
        'file'     : os.path.join(LOGINFOLD, 'david_easynews'),
        'settings' : os.path.join(ADDOND, 'plugin.video.david', 'settings.xml'),
        'default'  : 'easynews_user',
        'data'     : ['easynews_user', 'easynews_password'],
        'activate' : ''},
    'api-furk-david': {
        'name'     : 'Furk - David',
        'saved'    : 'api-furk-david',
        'plugin'   : 'plugin.video.david',
		'path'	 : os.path.join(ADDONS, 'plugin.video.david'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.david', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.david', 'fanart.jpg'),
        'file'     : os.path.join(LOGINFOLD, 'david_furk'),
        'settings' : os.path.join(ADDOND, 'plugin.video.david', 'settings.xml'),
        'default'  : 'furk_login',
        'data'     : ['furk_login', 'furk_password', 'furk_api_key'],
        'activate' : ''},
	'api-tmdb-exegesis': {
		'name'	 : 'Exegesis - TMDb Personal API Key',
		'plugin'   : 'plugin.video.exegesis',
		'saved'	: 'api-tmdb-exegesis',
		'path'	 : os.path.join(ADDONS, 'plugin.video.exegesis'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.exegesis', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exegesis', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-exegesis'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exegesis', 'settings.xml'),
		'default'  : 'tm.user',
		'data'	 : ['tm.user'],
		'activate' : ''},
	'api-imdb-exegesis': {
		'name'	 : 'Exegesis - IMDb Personal API Key',
		'plugin'   : 'plugin.video.exegesis',
		'saved'	: 'api-imdb-exegesis',
		'path'	 : os.path.join(ADDONS, 'plugin.video.exegesis'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.exegesis', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exegesis', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-imdb-exegesis'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exegesis', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'	 : ['imdb.user'],
		'activate' : ''},
	'api-fanart-tv-exegesis': {
		'name'	 : 'Exegesis - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.exegesis',
		'saved'	: 'api-fanart-tv-exegesis',
		'path'	 : os.path.join(ADDONS, 'plugin.video.exegesis'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.exegesis', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exegesis', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-fanart-tv-exegesis'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exegesis', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'	 : ['fanart.tv.user'],
		'activate' : ''},
	'api-tmdb-patriot': {
		'name'	 : 'Patriot - TMDb Personal API Key',
		'plugin'   : 'plugin.video.patriot',
		'saved'	: 'api-tmdb-patriot',
		'path'	 : os.path.join(ADDONS, 'plugin.video.patriot'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.patriot', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.patriot', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-patriot'),
		'settings' : os.path.join(ADDOND, 'plugin.video.patriot', 'settings.xml'),
		'default'  : 'tm.user',
		'data'	 : ['tm.user'],
		'activate' : ''},
	'api-imdb-patriot': {
		'name'	 : 'Patriot - IMDb Personal API Key',
		'plugin'   : 'plugin.video.patriot',
		'saved'	: 'api-imdb-patriot',
		'path'	 : os.path.join(ADDONS, 'plugin.video.patriot'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.patriot', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.patriot', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-imdb-patriot'),
		'settings' : os.path.join(ADDOND, 'plugin.video.patriot', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'	 : ['imdb.user'],
		'activate' : ''},
	'api-fanart-tv-patriot': {
		'name'	 : 'Patriot - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.patriot',
		'saved'	: 'api-fanart-tv-patriot',
		'path'	 : os.path.join(ADDONS, 'plugin.video.patriot'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.patriot', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.patriot', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-fanart-tv-patriot'),
		'settings' : os.path.join(ADDOND, 'plugin.video.patriot', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'	 : ['fanart.tv.user'],
		'activate' : ''},
	'api-tmdb-scrubsv2': {
		'name'	 : 'Scrubs v2 - TMDb Personal API Key',
		'plugin'   : 'plugin.video.scrubsv2',
		'saved'	: 'api-tmdb-scrubsv2',
		'path'	 : os.path.join(ADDONS, 'plugin.video.scrubsv2'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-scrubsv2'),
		'settings' : os.path.join(ADDOND, 'plugin.video.scrubsv2', 'settings.xml'),
		'default'  : 'tm.user',
		'data'	 : ['tm.user'],
		'activate' : ''},
	'api-imdb-scrubsv2': {
		'name'	 : 'Scrubs v2 - IMDb Personal API Key',
		'plugin'   : 'plugin.video.scrubsv2',
		'saved'	: 'api-imdb-scrubsv2',
		'path'	 : os.path.join(ADDONS, 'plugin.video.scrubsv2'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-imdb-scrubsv2'),
		'settings' : os.path.join(ADDOND, 'plugin.video.scrubsv2', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'	 : ['imdb.user'],
		'activate' : ''},
	'api-fanart-tv-scrubsv2': {
		'name'	 : 'Scrubs v2 - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.scrubsv2',
		'saved'	: 'api-fanart-tv-scrubsv2',
		'path'	 : os.path.join(ADDONS, 'plugin.video.scrubsv2'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-fanart-tv-scrubsv2'),
		'settings' : os.path.join(ADDOND, 'plugin.video.scrubsv2', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'	 : ['fanart.tv.user'],
		'activate' : ''},
	'api-tmdb-venom': {
		'name'	 : 'Venom - TMDb Personal API Key',
		'plugin'   : 'plugin.video.venom',
		'saved'	: 'api-tmdb-venom',
		'path'	 : os.path.join(ADDONS, 'plugin.video.venom'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.venom', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.venom', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-venom'),
		'settings' : os.path.join(ADDOND, 'plugin.video.venom', 'settings.xml'),
		'default'  : 'tm.user',
		'data'	 : ['tm.user'],
		'activate' : ''},
	'api-imdb-venom': {
		'name'	 : 'Venom - IMDb Personal API Key',
		'plugin'   : 'plugin.video.venom',
		'saved'	: 'api-imdb-venom',
		'path'	 : os.path.join(ADDONS, 'plugin.video.venom'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.venom', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.venom', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-imdb-venom'),
		'settings' : os.path.join(ADDOND, 'plugin.video.venom', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'	 : ['imdb.user'],
		'activate' : ''},
	'api-fanart-tv-venom': {
		'name'	 : 'Venom - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.venom',
		'saved'	: 'api-fanart-tv-venom',
		'path'	 : os.path.join(ADDONS, 'plugin.video.venom'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.venom', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.venom', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-fanart-tv-venom'),
		'settings' : os.path.join(ADDOND, 'plugin.video.venom', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'	 : ['fanart.tv.user'],
		'activate' : ''},
	'api-tmdb-judaea': {
		'name'	 : 'Judaea - TMDb Personal API Key',
		'plugin'   : 'plugin.video.judaea',
		'saved'	: 'api-tmdb-judaea',
		'path'	 : os.path.join(ADDONS, 'plugin.video.judaea'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.judaea', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.judaea', 'fanart.png'),
		'file'	 : os.path.join(LOGINFOLD, 'judaea_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.judaea', 'settings.xml'),
		'default'  : 'tmdb.apikey',
		'data'	 : ['tmdb.apikey'],
		'activate' : ''},
	'api-tvdb-judaea': {
		'name'	 : 'Judaea TVDB Personal API Key',
		'plugin'   : 'plugin.video.judaea',
		'saved'	: 'api-tvdb-judaea',
		'path'	 : os.path.join(ADDONS, 'plugin.video.judaea'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.judaea', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.judaea', 'fanart.png'),
		'file'	 : os.path.join(LOGINFOLD, 'judaea_tvdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.judaea', 'settings.xml'),
		'default'  : 'tvdb.apikey',
		'data'	 : ['tvdb.apikey', 'tvdb.jw', 'tvdb.expiry'],
		'activate' : ''},
	'api-fanart-tv-judaea': {
		'name'	 : 'Judaea - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.judaea',
		'saved'	: 'api-fanart-tv-judaea',
		'path'	 : os.path.join(ADDONS, 'plugin.video.judaea'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.judaea', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.judaea', 'fanart.png'),
		'file'	 : os.path.join(LOGINFOLD, 'judaea_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.judaea', 'settings.xml'),
		'default'  : 'fanart.apikey',
		'data'	 : ['fanart.apikey'],
		'activate' : ''},
	'api-tmdb-seren': {
		'name'	 : 'Seren - TMDB Personal API Key',
		'plugin'   : 'plugin.video.seren',
		'saved'	: 'api-tmdb-seren',
		'path'	 : os.path.join(ADDONS, 'plugin.video.seren'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.seren', 'ico-fox-gold-final.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.seren', 'fanart-fox-gold-final.png'),
		'file'	 : os.path.join(LOGINFOLD, 'seren_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.seren', 'settings.xml'),
		'default'  : 'tmdb.apikey',
		'data'	 : ['tmdb.apikey'],
		'activate' : ''},
	'api-tvdb-seren': {
		'name'	 : 'Seren - TVDB Personal API Key',
		'plugin'   : 'plugin.video.seren',
		'saved'	: 'api-tvdb-seren',
		'path'	 : os.path.join(ADDONS, 'plugin.video.seren'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.seren', 'ico-fox-gold-final.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.seren', 'fanart-fox-gold-final.png'),
		'file'	 : os.path.join(LOGINFOLD, 'seren_tvdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.seren', 'settings.xml'),
		'default'  : 'tvdb.apikey',
		'data'	 : ['tvdb.apikey', 'tvdb.jw', 'tvdb.expiry'],
		'activate' : ''},
	'api-fanart-tv-seren': {
		'name'	 : 'Seren - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.seren',
		'saved'	: 'api-fanart-tv-seren',
		'path'	 : os.path.join(ADDONS, 'plugin.video.seren'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.seren', 'ico-fox-gold-final.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.seren', 'fanart-fox-gold-final.png'),
		'file'	 : os.path.join(LOGINFOLD, 'seren_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.seren', 'settings.xml'),
		'default'  : 'fanart.apikey',
		'data'	 : ['fanart.apikey'],
		'activate' : ''},
	'api-tmdb-fen': {
		'name'	 : 'Fen - TMDb Personal API Key',
		'plugin'   : 'plugin.video.fen',
		'saved'	: 'api-tmdb-fen',
		'path'	 : os.path.join(ADDONS, 'plugin.video.fen'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.fen', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.fen', 'fanart.png'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-fen'),
		'settings' : os.path.join(ADDOND, 'plugin.video.fen', 'settings.xml'),
		'default'  : 'tmdb_api',
		'data'	 : ['tmdb_api'],
		'activate' : ''},
    'api-easynews-fen': {
        'name'     : 'EasyNews - Fen',
        'saved'    : 'api-easynews-fen',
        'plugin'   : 'plugin.video.fen',
		'path'	 : os.path.join(ADDONS, 'plugin.video.fen'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.fen', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(LOGINFOLD, 'fen_easynews'),
        'settings' : os.path.join(ADDOND, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'easynews_user',
        'data'     : ['easynews_user', 'easynews_password'],
        'activate' : ''},
    'api-furk-fen': {
        'name'     : 'Furk - Fen',
        'saved'    : 'api-furk-fen',
        'plugin'   : 'plugin.video.fen',
		'path'	 : os.path.join(ADDONS, 'plugin.video.fen'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.fen', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(LOGINFOLD, 'fen_furk'),
        'settings' : os.path.join(ADDOND, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'furk_login',
        'data'     : ['furk_login', 'furk_password', 'furk_api_key'],
        'activate' : ''},
	'api-tmdb-exodusredux': {
		'name'	 : 'Exodus Redux - TMDb Personal API Key',
		'plugin'   : 'plugin.video.exodusredux',
		'saved'	: 'api-tmdb-exodusredux',
		'path'	 : os.path.join(ADDONS, 'plugin.video.exodusredux'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.exodusredux', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-tmdb-exodusredux'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodusredux', 'settings.xml'),
		'default'  : 'tm.user',
		'data'	 : ['tm.user'],
		'activate' : ''},
	'api-imdb-exodusredux': {
		'name'	 : 'Exodus Redux - IMDb Personal API Key',
		'plugin'   : 'plugin.video.exodusredux',
		'saved'	: 'api-imdb-exodusredux',
		'path'	 : os.path.join(ADDONS, 'plugin.video.exodusredux'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.exodusredux', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-imdb-exodusredux'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodusredux', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'	 : ['imdb.user'],
		'activate' : ''},
	'api-fanart-tv-exodusredux': {
		'name'	 : 'Exodus Redux - Fanart.TV Personal API Key',
		'plugin'   : 'plugin.video.exodusredux',
		'saved'	: 'api-fanart-tv-exodusredux',
		'path'	 : os.path.join(ADDONS, 'plugin.video.exodusredux'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.exodusredux', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-fanart-tv-exodusredux'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodusredux', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'	 : ['fanart.tv.user'],
		'activate' : ''},
	'api-metaq': {
		'name'	 : 'MetaQ - TMDb Personal API Key',
		'plugin'   : 'plugin.video.metaq',
		'saved'	: 'api-metaq',
		'path'	 : os.path.join(ADDONS, 'plugin.video.metaq'),
		'icon'	 : os.path.join(ADDONS, 'plugin.video.metaq', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.metaq', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-metaq'),
		'settings' : os.path.join(ADDOND, 'plugin.video.metaq', 'settings.xml'),
		'default'  : 'tmdb_api',
		'data'	 : ['tmdb_api'],
		'activate' : ''},
	'api-eis': {
		'name'	 : 'ExtendedInfo Script',
		'plugin'   : 'script.extendedinfo',
		'saved'	: 'api-eis',
		'path'	 : os.path.join(ADDONS, 'script.extendedinfo'),
		'icon'	 : os.path.join(ADDONS, 'script.extendedinfo', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.extendedinfo', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-eis'),
		'settings' : os.path.join(ADDOND, 'script.extendedinfo', 'settings.xml'),
		'default'  : 'tmdb_username',
		'data'	 : ['tmdb_username', 'tmdb_password'],
		'activate' : ''},
	'api-opensubtitles': {
		'name'	 : 'OpenSubtitles',
		'plugin'   : 'service.subtitles.opensubtitles',
		'saved'	: 'api-opensubtitles',
		'path'	 : os.path.join(ADDONS, 'service.subtitles.opensubtitles'),
		'icon'	 : os.path.join(ADDONS, 'service.subtitles.opensubtitles', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'service.subtitles.opensubtitles', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'opensub_login'),
		'settings' : os.path.join(ADDOND, 'service.subtitles.opensubtitles', 'settings.xml'),
		'default'  : 'OSuser',
		'data'	 : ['OSuser', 'OSpass'],
		'activate' : ''},
	'api-orion': {
		'name'	 : 'Orion',
		'plugin'   : 'script.module.orion',
		'saved'	: 'api-orion',
		'path'	 : os.path.join(ADDONS, 'script.module.orion'),
		'icon'	 : os.path.join(ADDONS, 'script.module.orion', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.module.orion', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'orion'),
		'settings' : os.path.join(ADDOND, 'script.module.orion', 'settings.xml'),
		'default'  : 'account.key',
		'data'	 : ['account.key', 'account.valid'],
		'activate' : 'RunPlugin(plugin://script.module.orion/?action=settingsAccountLogin)'},
	'api-metahandler': {
		'name'	 : 'metahandler',
		'plugin'   : 'script.module.metahandler',
		'saved'	: 'api-metahandler',
		'path'	 : os.path.join(ADDONS, 'script.module.metahandler'),
		'icon'	 : os.path.join(ADDONS, 'script.module.metahandler', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.module.metahandler', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-metahandler'),
		'settings' : os.path.join(ADDOND, 'script.module.metahandler', 'settings.xml'),
		'default'  : 'tmdb_api_key',
		'data'	 : ['tmdb_api_key', 'omdb_api_key', 'tvdb_api_key'],
		'activate' : ''},
	'api-metadatautils': {
		'name'	 : 'script.module.metadatautils',
		'plugin'   : 'script.module.metadatautils',
		'saved'	: 'api-metadatautils',
		'path'	 : os.path.join(ADDONS, 'script.module.metadatautils'),
		'icon'	 : os.path.join(ADDONS, 'script.module.metadatautils', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.module.metadatautils', 'fanart.jpg'),
		'file'	 : os.path.join(LOGINFOLD, 'api-metadatautils'),
		'settings' : os.path.join(ADDOND, 'script.module.metadatautils', 'settings.xml'),
		'default'  : 'tmdb_apikey',
		'data'	 : ['fanarttv_apikey', 'omdbapi_apikey', 'tmdb_apikey'],
		'activate' : ''}
}

def loginUser(who):
	user=None
	if LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			try:
				add = wiz.addonId(LOGINID[who]['plugin'])
				user = add.getSetting(LOGINID[who]['default'])
			except:
				pass
	return user

def loginIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(LOGINFOLD):  os.makedirs(LOGINFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(LOGINID[log]['path']):
				try:
					addonid   = wiz.addonId(LOGINID[log]['plugin'])
					default   = LOGINID[log]['default']
					user	  = addonid.getSetting(default)
					if user == '' and do == 'update': continue
					updateLogin(do, log)
				except: pass
			else: wiz.log('[API Keys] %s(%s) is not installed' % (LOGINID[log]['name'],LOGINID[log]['plugin']), xbmc.LOGERROR)
		wiz.setS('loginlastsave', str(THREEDAYS))
	else:
		if LOGINID[who]:
			if os.path.exists(LOGINID[who]['path']):
				updateLogin(do, who)
		else: wiz.log('[API Keys] Invalid Entry: %s' % who, xbmc.LOGERROR)

def clearSaved(who, over=False):
	if who == 'all':
		for login in LOGINID:
			clearSaved(login,  True)
	elif LOGINID[who]:
		file = LOGINID[who]['file']
		if os.path.exists(file):
			os.remove(file)
			wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, LOGINID[who]['name']), '[COLOR %s]API Key: Removed![/COLOR]' % COLOR2, 2000, LOGINID[who]['icon'])
		wiz.setS(LOGINID[who]['saved'], '')
	if over == False: wiz.refresh()

def updateLogin(do, who):
	file	  = LOGINID[who]['file']
	settings  = LOGINID[who]['settings']
	data	  = LOGINID[who]['data']
	addonid   = wiz.addonId(LOGINID[who]['plugin'])
	saved	 = LOGINID[who]['saved']
	default   = LOGINID[who]['default']
	user	  = addonid.getSetting(default)
	suser	 = wiz.getS(saved)
	name	  = LOGINID[who]['name']
	icon	  = LOGINID[who]['icon']

	if do == 'update':
		if not user == '':
			try:
				with open(file, 'w') as f:
					for login in data:
						f.write('<login>\n\t<id>%s</id>\n\t<value>%s</value>\n</login>\n' % (login, addonid.getSetting(login)))
					f.close()
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Login Data: Saved![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Login Data] Unable to Update %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Login Data: Not Registered![/COLOR]' % COLOR2, 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<login><id>(.+?)</id><value>(.+?)</value></login>').findall(g)
			try:
				if len(match) > 0:
					for login, value in match:
						addonid.setSetting(login, value)
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Login: Restored![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Login Data] Unable to Restore %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		#else: wiz.LogNotify(name,'login Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
	elif do == 'clearaddon':
		wiz.log('%s SETTINGS: %s' % (name, settings), xbmc.LOGDEBUG)
		if os.path.exists(settings):
			try:
				f = open(settings, "r"); lines = f.readlines(); f.close()
				f = open(settings, "w")
				for line in lines:
					match = wiz.parseDOM(line, 'setting', ret='id')
					if len(match) == 0: f.write(line)
					else:
						if match[0] not in data: f.write(line)
						else: wiz.log('Removing Line: %s' % line, xbmc.LOGNOTICE)
				f.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Addon Data: Cleared![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Data] Unable to Clear Addon %s (%s)" % (who, str(e)), xbmc.LOGERROR)
	wiz.refresh()

def autoUpdate(who):
	if who == 'all':
		for log in LOGINID:
			if os.path.exists(LOGINID[log]['path']):
				autoUpdate(log)
	elif LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			u  = loginUser(who)
			su = wiz.getS(LOGINID[who]['saved'])
			n = LOGINID[who]['name']
			if u == None or u == '': return
			elif su == '': loginIt('update', who)
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to save the [COLOR %s]API[/COLOR] key for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "Addon: [COLOR springgreen][B]%s[/B][/COLOR]" % u, "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
					loginIt('update', who)
			else: loginIt('update', who)

def importlist(who):
	if who == 'all':
		for log in LOGINID:
			if os.path.exists(LOGINID[log]['file']):
				importlist(log)
	elif LOGINID[who]:
		if os.path.exists(LOGINID[who]['file']):
			d  = LOGINID[who]['default']
			sa = LOGINID[who]['saved']
			su = wiz.getS(sa)
			n  = LOGINID[who]['name']
			f  = open(LOGINID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<login><id>%s</id><value>(.+?)</value></login>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to import the [COLOR %s]Login[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "File: [COLOR springgreen][B]%s[/B][/COLOR]" % m[0], "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)), xbmc.LOGNOTICE)
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)

def activateLogin(who):
	if LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			act	 = LOGINID[who]['activate']
			addonid = wiz.addonId(LOGINID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(LOGINID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % LOGINID[who]['name'])
	else:
		wiz.refresh()
		return
	check = 0
	while loginUser(who) == None or loginUser(who) == "":
		if check == 30: break
		check += 1
		time.sleep(10)
	wiz.refresh()
