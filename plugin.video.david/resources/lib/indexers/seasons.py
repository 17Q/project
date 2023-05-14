# -*- coding: utf-8 -*-
import metadata
from modules import kodi_utils, settings
from modules.utils import adjust_premiered_date, get_datetime
from modules.watched_status import get_watched_info_tv, get_watched_status_season
# from modules.kodi_utils import logger

make_listitem, build_url, external_browse, ls, ts = kodi_utils.make_listitem, kodi_utils.build_url, kodi_utils.external_browse, kodi_utils.local_string, kodi_utils.translate_path
sys, add_items, set_content, end_directory, set_view_mode = kodi_utils.sys, kodi_utils.add_items, kodi_utils.set_content, kodi_utils.end_directory, kodi_utils.set_view_mode
adjust_premiered_date_function, get_datetime_function, get_watched_status, get_watched_info = adjust_premiered_date, get_datetime, get_watched_status_season, get_watched_info_tv
metadata_user_info, watched_indicators_info, show_unaired_info = settings.metadata_user_info, settings.watched_indicators, settings.show_unaired
get_art_provider, show_specials, use_season_title_info = settings.get_art_provider, settings.show_specials, settings.use_season_title
poster_empty, fanart_empty = kodi_utils.empty_poster, kodi_utils.addon_fanart
david_str, trakt_str, season_str, watched_str, unwatched_str, extras_str, options_str = ls(32036), ls(32037), ls(32537), ls(32642), ls(32643), ls(32645), ls(32646)
string, run_plugin, unaired_label, tmdb_poster = str, 'RunPlugin(%s)', '[COLOR red][I]%s[/I][/COLOR]', 'https://image.tmdb.org/t/p/'

def build_season_list(params):
	def _process():
		running_ep_count = total_aired_eps
		for item in season_data:
			try:
				listitem = make_listitem()
				set_properties = listitem.setProperties
				cm = []
				cm_append = cm.append
				item_get = item.get
				name, overview = item_get('name'), item_get('overview')
				poster_path, air_date = item_get('poster_path'), item_get('air_date')
				season_number, episode_count = item_get('season_number'), item_get('episode_count')
				poster =  ''.join([tmdb_poster, image_resolution, poster_path]) if poster_path is not None else show_poster
				if season_number == 0: unaired = False
				elif episode_count == 0: unaired = True
				elif season_number != total_seasons: unaired = False
				else:
					first_airdate = adjust_premiered_date_function(air_date, 0)[0]
					if not first_airdate or current_date < first_airdate: unaired = True
					else: unaired = False
				if unaired:
					if not show_unaired: continue
					episode_count = 0
				else:
					running_ep_count -= episode_count
					if running_ep_count < 0: episode_count = running_ep_count + episode_count
				try: year = air_date.split('-')[0]
				except: year = show_year
				plot = overview or show_plot
				title = name if use_season_title and name else ' '.join([season_str, string(season_number)])
				if unaired: title = unaired_label % title
				playcount, overlay, watched, unwatched = get_watched_status(watched_info, str_tmdb_id, season_number, episode_count)
				try: progress = int((float(watched)/episode_count)*100)
				except: progress = 0
				url_params = build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': season_number})
				extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'tvshow', 'is_widget': is_widget})
				options_params = build_url({'mode': 'options_menu_choice', 'content': 'season', 'tmdb_id': tmdb_id, 'poster': show_poster, 'is_widget': is_widget})
				cm_append((extras_str, run_plugin % extras_params))
				cm_append((options_str, run_plugin % options_params))
				if not playcount:
					watched_params = build_url({'mode': 'mark_as_watched_unwatched_season', 'action': 'mark_as_watched', 'title': show_title, 'year': show_year,
														  'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season_number})
					cm_append((watched_str % watched_title, run_plugin % watched_params))
				if watched:
					if hide_watched: continue
					unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_season', 'action': 'mark_as_unwatched', 'title': show_title, 'year': show_year,
															'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season_number})
					cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
				listitem.setLabel(title)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'poster': poster, 'season.poster': poster, 'icon': poster, 'thumb': poster, 'fanart': fanart, 'banner': banner, 'landscape': landscape,
								'clearlogo': clearlogo, 'clearart': clearart, 'tvshow.poster': show_poster, 'tvshow.clearlogo': clearlogo, 'tvshow.clearart': clearart})
				try: listitem.setCast(cast)
				except: pass
				listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': str_tmdb_id, 'tvdb': str_tvdb_id})
				listitem.setInfo('video', {'mediatype': 'season', 'trailer': trailer, 'title': title, 'size': '0', 'duration': episode_run_time, 'plot': plot,
								'rating': rating, 'premiered': premiered, 'studio': studio, 'year': year,'genre': genre, 'mpaa': mpaa, 'tvshowtitle': show_title,
								'imdbnumber': imdb_id, 'votes': votes, 'season': season_number,'playcount': playcount, 'overlay': overlay})
				set_properties({'david_widget': 'false', 'watchedepisodes': string(watched), 'unwatchedepisodes': string(unwatched),
								'totalepisodes': string(episode_count), 'watchedprogress': string(progress)})
				if is_widget:
					set_properties({'david_widget': 'true', 'david_playcount': string(playcount), 'david_extras_params': extras_params, 'david_options_params': options_params})
				yield (url_params, listitem, True)
			except: pass
	handle = int(sys.argv[1])
	try:
		meta_user_info = metadata_user_info()
		watched_indicators = watched_indicators_info()
		watched_info = get_watched_info(watched_indicators)
		show_unaired = show_unaired_info()
		is_widget = external_browse()
		current_date = get_datetime_function()
		image_resolution = meta_user_info['image_resolution']['poster']
		poster_main, poster_backup, fanart_main, fanart_backup, clearlogo_main, clearlogo_backup = get_art_provider()
		fanart_enabled = meta_user_info['extra_fanart_enabled']
		hide_watched = is_widget and meta_user_info['widget_hide_watched']
		meta = metadata.tvshow_meta('tmdb_id', params['tmdb_id'], meta_user_info, current_date)
		meta_get = meta.get
		season_data = meta_get('season_data')
		tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
		str_tmdb_id, str_tvdb_id = string(tmdb_id), string(tvdb_id)
		show_title, show_year, show_plot = meta_get('title'), meta_get('year'), meta_get('plot')
		show_poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
		fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
		clearlogo = meta_get(clearlogo_main) or meta_get(clearlogo_backup) or ''
		if fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearart'), meta_get('landscape')
		else: banner, clearart, landscape = '', '', ''
		cast, mpaa, votes = meta_get('cast', []), meta_get('mpaa'), meta_get('votes')
		trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
		episode_run_time, rating, premiered = meta_get('episode_run_time'), meta_get('rating'), meta_get('premiered')
		total_seasons = meta_get('total_seasons')
		total_aired_eps = meta_get('total_aired_eps')
		if not show_specials(): season_data = [i for i in season_data if not i['season_number'] == 0]
		season_data.sort(key=lambda k: k['season_number'])
		use_season_title = use_season_title_info()
		watched_title = trakt_str if watched_indicators == 1 else david_str
		add_items(handle, list(_process()))
	except: pass
	set_content(handle, 'seasons')
	end_directory(handle, False if is_widget else None)
	if not is_widget: set_view_mode('view.seasons', 'seasons')