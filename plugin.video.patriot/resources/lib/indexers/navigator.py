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


import os,sys
import xbmc, xbmcaddon, xbmcgui

import six

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache
from resources.lib.modules import api_keys

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065)


class navigator:

    ADDON_ID      = xbmcaddon.Addon().getAddonInfo('id')
    HOMEPATH      = xbmc.translatePath('special://home/')
    ADDONSPATH    = os.path.join(HOMEPATH, 'addons')
    THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
    LOCALNEWS     = os.path.join(THISADDONPATH, 'news.txt')


    def root(self):
        if self.getMenuEnabled('navi.movies') == True:
            self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.tvShows') == True:
            self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.movieWidget') == True:
            self.addDirectoryItem('My Movies (Trakt)', 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
#         if not control.setting('lists.widget') == '0':
#             self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

        if self.getMenuEnabled('navi.tvWidget') == True:
            self.addDirectoryItem('My TV Shows (Trakt)', 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')
#             self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if self.getMenuEnabled('navi.movieNew') == True:
            if not control.setting('movie.widget') == '0':
                self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if self.getMenuEnabled('navi.episodeNew') == True:
            if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
                self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

        if not control.setting('furk.api') == '':
            self.addDirectoryItem('Furk.net', 'furkNavigator', 'movies.png', 'movies.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        if self.getMenuEnabled('navi.search') == True:
            self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')

        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()


    def furk(self):
        self.addDirectoryItem('User Files', 'furkUserFiles', 'mymovies.png', 'DefaultVideoPlaylists.png')
        self.addDirectoryItem('Search', 'furkSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.endDirectory()


    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True


    def movies(self, lite=False):
        if self.getMenuEnabled('navi.moviesTheaters') == True:
            self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')

        if self.getMenuEnabled('navi.moviesRecently') == True:
            self.addDirectoryItem(32580, 'movies&url=added', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if self.getMenuEnabled('navi.moviesLatest') == True:
            self.addDirectoryItem(32321, 'movies&url=featured', 'featured.png', 'DefaultRecentlyAddedMovies.png')

        if self.getMenuEnabled('navi.moviesPopular') == True:
            self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesTrending') == True:
            self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')

        if self.getMenuEnabled('navi.moviesGenre') == True:
            self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesMales') == True:
            self.addDirectoryItem('Most Popular Actors', 'movieMales', 'people.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesFemales') == True:
            self.addDirectoryItem('Most Popular Actresses', 'movieFemales', 'people.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesPersons') == True:
            self.addDirectoryItem('Most Popular People', 'moviePersons', 'people.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesBoxsets') == True:
            self.addDirectoryItem('Boxsets', 'movieBoxsets', 'imdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesTrilogies') == True:
            self.addDirectoryItem('Trilogies', 'movieTrilogies', 'imdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesCar') == True:
            self.addDirectoryItem('Car Movies', 'movies&url=movieCar', 'car.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesPrison') == True:
            self.addDirectoryItem('Prison Movies', 'movies&url=moviePrison', 'movies-boxsets.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesXmas') == True:
            self.addDirectoryItem('Christmas Movies', 'movies&url=movieXmas', 'christmas.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesKid') == True:
            self.addDirectoryItem('Kid Movies', 'movies&url=movieKid', 'kids.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesDisney') == True:
            self.addDirectoryItem('Disney Movies', 'movies&url=movieDisney', 'disney.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesDc') == True:
            self.addDirectoryItem('DC Comics Movies', 'movies&url=movieDc', 'superhero.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesMarvel') == True:
            self.addDirectoryItem('Marvel Movies', 'movies&url=movieMarvel', 'superhero2.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesYears') == True:
            self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesDecades') == True:
            self.addDirectoryItem(32123, 'movieDecades', 'years.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesMosts') == True:
            self.addDirectoryItem('Mosts', 'movieMosts', 'featured.png', 'playlist.jpg')

        if self.getMenuEnabled('navi.moviesVoted') == True:
            self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesHighlyRated') == True:
            self.addDirectoryItem(32023, 'movies&url=rating', 'highly-rated.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesLanguages') == True:
            self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesCertificates') == True:
            self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesOscars') == True:
            self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesBoxOffice') == True:
            self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movieslistWidget') == True:
            if lite == False:
                if not control.setting('lists.widget') == '0':
                    self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

        if self.getMenuEnabled('navi.moviesPerson') == True:
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.moviesSearch') == True:
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32094, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            if control.setting('imdb.sort.order') == '1':
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)
            else:
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32094, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            if control.setting('imdb.sort.order') == '1':
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)
            else:
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultAddonsSearch.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultAddonsSearch.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        if self.getMenuEnabled('navi.tvPopular') == True:
            self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvTrending') == True:
            self.addDirectoryItem(32017, 'tvshows&url=trending', 'people-watching.png', 'DefaultRecentlyAddedEpisodes.png')

        if self.getMenuEnabled('navi.tvGenres') == True:
            self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvNetworks') == True:
            self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvLanguages') == True:
            self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvCertificates') == True:
            self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvMost') == True:
            self.addDirectoryItem('Mosts', 'tvMosts', 'featured.png', 'playlist.jpg')

        if self.getMenuEnabled('navi.tvRating') == True:
            self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvViews') == True:
            self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvAiring') == True:
            self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvActive') == True:
            self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvPremier') == True:
            self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvAdded') == True:
            self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        if self.getMenuEnabled('navi.tvCalendar') == True:
            self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')

        if self.getMenuEnabled('navi.tvlistWidget') == True:
            if lite == False:
                if not control.setting('lists.widget') == '0':
                    self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if self.getMenuEnabled('navi.tvPerson') == True:
            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.tvSearch') == True:
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def mytvshows(self, lite=False):
        try:
            self.accountCheck()

            if traktCredentials == True and imdbCredentials == True:

                self.addDirectoryItem(32094, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                if control.setting('imdb.sort.order') == '1':
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')
                else:
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

            elif traktCredentials == True:
                self.addDirectoryItem(32094, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

            elif imdbCredentials == True:
                if control.setting('imdb.sort.order') == '1':
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')
                else:
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

            if lite == False:
                self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultAddonsSearch.png')
                self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultAddonsSearch.png')
            self.endDirectory()
        except:
            print("ERROR")


    def imdbLists(self):
        self.addDirectoryItem('Car Movies', 'movies&url=movieCar', 'car.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Prison Movies', 'movies&url=moviePrison', 'movies-boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Christmas Movies', 'movies&url=movieXmas', 'christmas.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Disney Movies', 'movies&url=movieDisney', 'disney.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kid Movies', 'movies&url=movieKid', 'kids.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('DC Comics Movies', 'movies&url=movieDc', 'superhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Marvel Movies', 'movies&url=movieMarvel', 'superhero2.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
       

    def tools(self):
        self.addDirectoryItem('[B]Settings[/B] : General', 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Navigation', 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Playback', 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Trakt', 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : API Keys', 'openSettings&query=4.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Settings[/B] : Premium Accounts', 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Patriot[/B] : Library', 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Patriot[/B] : Viewtypes', 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Patriot[/B] : News, Updates & Information', 'newsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Patriot[/B] : Cache Functions', 'cacheNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Patriot[/B] : Log Functions', 'logNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Patriot[/B] : Clean Settings File', 'cleanSettings', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)

        if not control.condVisibility('System.HasAddon(script.module.orion)'):
            self.addDirectoryItem('[B]Orion[/B] : Install', 'installOrion', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        else:
            self.addDirectoryItem('[B]Orion[/B] : Settings', 'orionsettings', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)

        self.addDirectoryItem('[B]Trakt[/B] : Authorize Patriot With Trakt', 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]ResolveURL[/B] : Configure ResolveURL Settings', 'smuSettings', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Configure Oath Scraper Settings[/B] : OathScraper Settings', 'oathscrapersettings', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()


    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png', isFolder=False)
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', isFolder=False)
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', isFolder=False)
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', isFolder=False)

        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def cache_functions(self):
        self.addDirectoryItem(32604, 'clearCacheSearch&select=all', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32116, 'clearDebridCheck', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32611, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)

        self.endDirectory()


    def log_functions(self):
        self.addDirectoryItem('[B]Patriot[/B] : View Log', 'viewLog', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[B]Patriot[/B] : Empty Log', 'emptyLog', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultAddonsSearch.png')

        self.endDirectory()


    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001), 'movies'), (control.lang(32002), 'tvshows'), (control.lang(32054), 'seasons'), (control.lang(32038), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059)
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042), sound=True, icon='WARNING')
            #sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')


    def clearCacheMeta(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')


    def clearCacheProviders(self):
#        yes = control.yesnoDialog(control.lang(32056))
#        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')


    def clearCacheSearch(self, select):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_search(select)
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')


    def clearDebridCheck(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_debrid()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')


    def clearCacheAll(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')


    def uploadLog(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import log_utils
        log_utils.upload_log()


    def emptyLog(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import log_utils
        log_utils.empty_log()


    def news(self):
            r = open(self.LOCALNEWS)
            compfile = r.read()
            self.showText('News - Updates - Information', compfile)


    def showText(self, heading, text):
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel(heading)
                win.getControl(5).setText(text)
                quit()
                return
            except: pass


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        try: name = control.lang(name)
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        try: item = control.item(label=name, offscreen=True)
        except: item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
        item.setInfo(type='video', infoLabels={'plot': '[CR]'})
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self, cache=True):
        syshandle = int(sys.argv[1])
        control.content(syshandle, '')
        control.directory(syshandle, cacheToDisc=cache)
