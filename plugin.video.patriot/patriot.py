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


from six.moves import urllib_parse


params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

status = params.get('status')

rtype = params.get('rtype')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ('0', '1') else 0


if action == None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()


elif action == 'newsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().news()

elif action == 'furkNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().furk()

elif action == 'furkMetaSearch':
    from resources.lib.indexers import furk
    furk.furk().furk_meta_search(url)

elif action == 'furkSearch':
    from resources.lib.indexers import furk
    furk.furk().search()

elif action == 'furkUserFiles':
    from resources.lib.indexers import furk
    furk.furk().user_files()

elif action == 'furkSearchNew':
    from resources.lib.indexers import furk
    furk.furk().search_new()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'libraryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'cacheNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().cache_functions()

elif action == 'logNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().log_functions()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'clearCacheProviders':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheProviders()

elif action == 'clearDebridCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().clearDebridCheck()

elif action == 'clearCacheSearch':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheSearch(select)

elif action == 'clearAllCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheAll()

elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'uploadLog':
    from resources.lib.indexers import navigator
    navigator.navigator().uploadLog()

elif action == 'emptyLog':
    from resources.lib.indexers import navigator
    navigator.navigator().emptyLog()

elif action == 'viewLog':
    from resources.lib.modules import log_utils
    log_utils.view_log()

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'movieSearchnew':
    from resources.lib.indexers import movies
    movies.movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(name)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieMosts':
    from resources.lib.indexers import movies
    movies.movies().mosts()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'movieDecades':
    from resources.lib.indexers import movies
    movies.movies().decades()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieBoxsets':
    from resources.lib.indexers import movies
    movies.movies().boxsets()

elif action == 'movieTrilogies':
    from resources.lib.indexers import movies
    movies.movies().trilogies()

elif action == 'movieMales':
    from resources.lib.indexers import movies
    movies.movies().males(url)

elif action == 'movieFemales':
    from resources.lib.indexers import movies
    movies.movies().females(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvSearchnew':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(name)

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvMosts':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().mosts()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tmdb, meta)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tmdb, meta, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tmdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tmdb, season, query)

elif action == 'yt_trailer':
    from resources.lib.modules import control, trailer
    if not control.condVisibility('System.HasAddon(plugin.video.youtube)'):
        control.installAddon('plugin.video.youtube')
    trailer.YT_trailer().play(name, url, tmdb, imdb, season, episode, windowedtrailer)

elif action == 'tmdb_trailer':
    from resources.lib.modules import control, trailer
    if not control.condVisibility('System.HasAddon(plugin.video.youtube)'):
        control.installAddon('plugin.video.youtube')
    trailer.TMDb_trailer().play(tmdb, imdb, season, episode, windowedtrailer)

elif action == 'imdb_trailer':
    from resources.lib.modules import trailer
    trailer.IMDb_trailer().play(imdb, name, tmdb, season, episode, windowedtrailer)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tmdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'smuSettings':
    try:
        import resolveurl
        resolveurl.display_settings()
    except: pass

elif action == 'patriotscrapersettings':
    from resources.lib.modules import control
    control.openSettings('0.0', 'script.module.patriotscrapers')

elif action == 'installOrion':
    from resources.lib.modules import control
    control.installAddon('script.module.orion')
    control.sleep(200)
    control.refresh()

elif action == 'orionsettings':
    from resources.lib.modules import control
    control.openSettings('0.0', 'script.module.orion')

elif action == 'download':
    import simplejson as json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'play':
    from resources.lib.modules import control
    control.busy()
    from resources.lib.modules import sources
    sources.sources().play(title, year, imdb, tmdb, season, episode, tvshowtitle, premiered, meta, select, unfiltered=False)

elif action == 'playUnfiltered':
    from resources.lib.modules import control
    control.busy()
    from resources.lib.modules import sources
    sources.sources().play(title, year, imdb, tmdb, season, episode, tvshowtitle, premiered, meta, select, unfiltered=True)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'moviesToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libmovies().silent(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tmdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'tvshowsToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libtvshows().silent(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()

elif action == 'syncTraktStatus':
    from resources.lib.modules import trakt
    trakt.syncTraktStatus()

elif action == 'changelog':
    from resources.lib.modules import changelog
    changelog.get()	

elif action == 'cleanSettings':
    from resources.lib.modules import control
    control.clean_settings()

elif action == 'random':
    from sys import argv
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = argv[0]+'?action=play'
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tmdb, meta, season, create_directory=False)
        r = argv[0]+'?action=play'
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tmdb, None, create_directory=False)
        r = argv[0]+'?action=random&rtype=episode'
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = argv[0]+'?action=random&rtype=season'
    from random import randint
    import simplejson as json
    try:
        from resources.lib.modules import control
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tmdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == 'show' and p == 'tvshowtitle':
                try: r += '&'+p+'='+urllib_parse.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                if rtype == 'movie':
                    rlist[rand]['title'] = rlist[rand]['originaltitle']
                elif rtype == 'episode':
                    rlist[rand]['tvshowtitle'] = urllib_parse.unquote_plus(rlist[rand]['tvshowtitle'])
                try: r += '&'+p+'='+urllib_parse.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib_parse.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta={}'
        if rtype == 'movie':
            try: control.infoDialog('%s (%s)' % (rlist[rand]['title'], rlist[rand]['year']), control.lang(32536), time=20000)
            except: pass
        elif rtype == 'episode':
            try: control.infoDialog('%s - %01dx%02d . %s' % (urllib_parse.unquote_plus(rlist[rand]['tvshowtitle']), int(rlist[rand]['season']), int(rlist[rand]['episode']), rlist[rand]['title']), control.lang(32536), time=20000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        from resources.lib.modules import control
        control.infoDialog(control.lang(32537), time=8000)
