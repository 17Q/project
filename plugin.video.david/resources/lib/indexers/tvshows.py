# -*- coding: utf-8 -*-
from metadata import tvshow_meta
from modules import kodi_utils, settings
from modules.utils import manual_function_import, get_datetime, make_thread_list_enumerate
from modules.watched_status import get_watched_info_tv, get_watched_status_tvshow
# logger = kodi_utils.logger

meta_function, get_datetime_function, add_item, select_dialog = tvshow_meta, get_datetime, kodi_utils.add_item, kodi_utils.select_dialog
get_watched_function, get_watched_info_function = get_watched_status_tvshow, get_watched_info_tv
set_content, end_directory, set_view_mode, get_infolabel = kodi_utils.set_content, kodi_utils.end_directory, kodi_utils.set_view_mode, kodi_utils.get_infolabel
string, ls, sys, external_browse, add_items = str, kodi_utils.local_string, kodi_utils.sys, kodi_utils.external_browse, kodi_utils.add_items
make_listitem, build_url, remove_meta_keys, dict_removals = kodi_utils.make_listitem, kodi_utils.build_url, kodi_utils.remove_meta_keys, kodi_utils.tvshow_dict_removals
metadata_user_info, watched_indicators = settings.metadata_user_info, settings.watched_indicators
sleep, extras_open_action, get_art_provider, default_all_episodes = kodi_utils.sleep, settings.extras_open_action, settings.get_art_provider, settings.default_all_episodes
item_jump, item_next, poster_empty, fanart_empty = kodi_utils.item_jump, kodi_utils.item_next, kodi_utils.empty_poster, kodi_utils.addon_fanart
max_threads, widget_hide_next_page = settings.max_threads, settings.widget_hide_next_page
david_str, trakt_str, watched_str, unwatched_str, exit_str, nextpage_str, browse_str, jumpto_str = ls(32036), ls(32037), ls(32642), ls(32643), ls(32650), ls(32799), ls(32652), ls(32964)
extras_str, options_str = ls(32645), ls(32646)
run_plugin, container_update, container_refresh = 'RunPlugin(%s)', 'Container.Update(%s)', 'Container.Refresh(%s)'
tmdb_main = ('tmdb_tv_popular', 'tmdb_tv_premieres', 'tmdb_tv_airing_today','tmdb_tv_on_the_air','tmdb_tv_upcoming')
trakt_main = ('trakt_tv_trending', 'trakt_recommendations', 'trakt_tv_most_watched')
trakt_personal, imdb_personal = ('trakt_collection', 'trakt_watchlist', 'trakt_collection_lists'), ('imdb_watchlist', 'imdb_user_list_contents', 'imdb_keywords_list_contents')
tmdb_special_dict = {'tmdb_tv_languages': 'language', 'tmdb_tv_networks': 'network_id', 'tmdb_tv_year': 'year', 'tmdb_tv_recommendations': 'tmdb_id',
					'tmdb_tv_genres': 'genre_id', 'tmdb_tv_search': 'query'}
personal_dict = {'in_progress_tvshows': ('modules.watched_status', 'get_in_progress_tvshows'), 'favorites_tvshows': ('modules.favorites', 'retrieve_favorites'),
				'watched_tvshows': ('modules.watched_status', 'get_watched_items')}

class TVShows:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.id_type, self.list, self.action = self.params_get('id_type', 'tmdb_id'), self.params_get('list', []), self.params_get('action', None)
		self.items, self.new_page, self.total_pages, self.is_widget, self.max_threads = [], {}, None, external_browse(), max_threads()
		self.append = self.items.append
	
	def fetch_list(self):
		try:
			self.handle, view_mode, content_type, mode = int(sys.argv[1]), 'view.tvshows', 'tvshows', self.params_get('mode')
			try: page_no = int(self.params_get('new_page', '1'))
			except ValueError: page_no = self.params_get('new_page')
			if self.action in personal_dict: var_module, import_function = personal_dict[self.action]
			else: var_module, import_function = 'apis.%s_api' % self.action.split('_')[0], self.action
			try: function = manual_function_import(var_module, import_function)
			except: pass
			if self.action in tmdb_main:
				data = function(page_no)
				self.list = [i['id'] for i in data['results']]
				if data['total_pages'] > page_no: self.new_page = {'new_page': string(page_no + 1)}
			elif self.action in tmdb_special_dict:
				key = tmdb_special_dict[self.action]
				function_var = self.params_get(key, None)
				if not function_var: return
				data = function(function_var, page_no)
				self.list = [i['id'] for i in data['results']]
				if data['total_pages'] > page_no: self.new_page = {'new_page': string(page_no + 1), key: function_var}
			elif self.action in personal_dict:
				data, total_pages = function('tvshow', page_no)
				self.list = [i['media_id'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				if total_pages > page_no: self.new_page = {'new_page': string(page_no + 1)}
			elif self.action in trakt_main:
				self.id_type = 'trakt_dict'
				data = function(page_no)
				try: self.list = [i['show']['ids'] for i in data]
				except: self.list = [i['ids'] for i in data]
				if self.action != 'trakt_recommendations': self.new_page = {'new_page': string(page_no + 1)}
			elif self.action in trakt_personal:
				self.id_type = 'trakt_dict'
				data, total_pages = function('shows', page_no)
				self.list = [i['media_ids'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				try:
					if total_pages > page_no: self.new_page = {'new_page': string(page_no + 1)}
				except: pass
			elif self.action in imdb_personal:
				self.id_type = 'imdb_id'
				list_id = self.params_get('list_id', None)
				data, next_page = function('tvshow', list_id, page_no)
				self.list = [i['imdb_id'] for i in data]
				if next_page: self.new_page = {'list_id': list_id, 'new_page': string(page_no + 1)}
			elif self.action == 'tmdb_tv_discover':
				from indexers.discover import set_history
				name, query = self.params['name'], self.params['query']
				if page_no == 1: set_history('tvshow', name, query)
				data = function(query, page_no)
				self.list = [i['id'] for i in data['results']]
				if data['page'] < data['total_pages']: self.new_page = {'query': query, 'name': name, 'new_page': string(data['page'] + 1)}
			elif self.action == 'trakt_tv_certifications':
				self.id_type = 'trakt_dict'
				data = function(self.params['certification'], page_no)
				self.list = [i['show']['ids'] for i in data]
				self.new_page = {'new_page': string(page_no + 1), 'certification': self.params['certification']}
			if self.total_pages and not self.is_widget:
				url_params = {'mode': 'build_navigate_to_page', 'media_type': 'TV Shows', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode,
							'transfer_action': self.action, 'query': self.params_get('search_name', ''), 'actor_id': self.params_get('actor_id', '')}
				self.add_dir(url_params, 'navigate_to_page', jumpto_str, item_jump, False)
			add_items(self.handle, self.worker())
			if self.new_page and not self.widget_hide_next_page:
					self.new_page.update({'mode': mode, 'action': self.action, 'exit_list_params': self.exit_list_params})
					self.add_dir(self.new_page)
		except: pass
		set_content(self.handle, content_type)
		end_directory(self.handle, False if self.is_widget else None)
		if not self.is_widget: set_view_mode(view_mode, content_type)

	def build_tvshow_content(self, item_position, _id):
		try:
			cm = []
			cm_append = cm.append
			meta, tmdb_id, playcount, total_seasons, total_watched, total_unwatched, total_aired_eps, progress = self.get_meta(_id)
			meta_get = meta.get
			if meta_get('blank_entry', False): return
			listitem = make_listitem()
			set_properties = listitem.setProperties
			title, year, trailer = meta_get('title'), meta_get('year'), meta_get('trailer')
			tvdb_id, imdb_id = meta_get('tvdb_id'), meta_get('imdb_id')
			poster = meta_get(self.poster_main) or meta_get(self.poster_backup) or poster_empty
			fanart = meta_get(self.fanart_main) or meta_get(self.fanart_backup) or fanart_empty
			clearlogo = meta_get(self.clearlogo_main) or meta_get(self.clearlogo_backup) or ''
			options_params = build_url({'mode': 'options_menu_choice', 'content': 'tvshow', 'tmdb_id': tmdb_id, 'poster': poster, 'is_widget': self.is_widget})
			extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'tvshow', 'is_widget': self.is_widget})
			if self.fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearlogo'), meta_get('landscape')
			else: banner, clearart, landscape = '', '', ''
			if self.all_episodes:
				if self.all_episodes == 1 and total_seasons > 1: url_params = build_url({'mode': 'build_season_list', 'tmdb_id': tmdb_id})
				else: url_params = build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 'all'})
			else: url_params = build_url({'mode': 'build_season_list', 'tmdb_id': tmdb_id})
			if self.open_extras:
				cm_append((browse_str, container_update % url_params))
				url_params = extras_params
			else: cm_append((extras_str, run_plugin % extras_params))
			cm_append((options_str, run_plugin % options_params))
			if not playcount:
				watched_params = build_url({'mode': 'mark_as_watched_unwatched_tvshow', 'action': 'mark_as_watched', 'title': title, 'year': year,
													'tmdb_id': tmdb_id, 'imdb_id': imdb_id, 'tvdb_id': tvdb_id})
				cm_append((watched_str % self.watched_title, run_plugin % watched_params))
			elif self.widget_hide_watched: return
			if total_watched:
				unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_tvshow', 'action': 'mark_as_unwatched', 'title': title, 'year': year,
													'tmdb_id': tmdb_id, 'imdb_id': imdb_id, 'tvdb_id': tvdb_id})
				cm_append((unwatched_str % self.watched_title, run_plugin % unwatched_params))
			cm_append((exit_str, container_refresh % self.exit_list_params))
			listitem.setLabel(title)
			listitem.addContextMenuItems(cm)
			listitem.setCast(meta_get('cast', []))
			listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'thumb': landscape,
							'landscape': landscape, 'tvshow.poster': poster, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo})
			listitem.setInfo('video', remove_meta_keys(meta, dict_removals))
			set_properties({'david_widget': 'false', 'watchedepisodes': string(total_watched), 'unwatchedepisodes': string(total_unwatched), 'watchedprogress': string(progress),
							'totalepisodes': string(total_aired_eps), 'totalseasons': string(total_seasons), 'david_sort_order': string(item_position)})
			if self.is_widget:
				set_properties({'david_widget': 'true', 'david_playcount': string(playcount), 'david_extras_params': extras_params, 'david_options_params': options_params})
			self.append((url_params, listitem, self.is_folder))
		except: pass

	def get_meta(self, _id):
		meta = meta_function(self.id_type, _id, self.meta_user_info, self.current_date)
		if not meta: return
		tmdb_id, total_seasons, total_aired_eps = meta['tmdb_id'], meta['total_seasons'], meta['total_aired_eps']
		playcount, overlay, total_watched, total_unwatched = get_watched_function(self.watched_info, string(tmdb_id), total_aired_eps)
		try: progress = int((float(total_watched)/total_aired_eps)*100)
		except: progress = 0
		meta.update({'playcount': playcount, 'overlay': overlay})
		return meta, tmdb_id, playcount, total_seasons, total_watched, total_unwatched, total_aired_eps, progress

	def worker(self):
		self.exit_list_params = self.params_get('exit_list_params', None) or get_infolabel('Container.FolderPath')
		self.current_date = get_datetime_function()
		self.meta_user_info = metadata_user_info()
		self.watched_indicators = watched_indicators()
		self.watched_info = get_watched_info_function(self.watched_indicators)
		self.all_episodes = default_all_episodes()
		self.open_extras = extras_open_action('tvshow')
		self.fanart_enabled = self.meta_user_info['extra_fanart_enabled']
		self.widget_hide_next_page = False if not self.is_widget else widget_hide_next_page()
		self.widget_hide_watched = self.is_widget and self.meta_user_info['widget_hide_watched']
		self.watched_title = trakt_str if self.watched_indicators == 1 else david_str
		self.is_folder = False if self.open_extras else True
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup, self.clearlogo_main, self.clearlogo_backup = get_art_provider()
		threads = list(make_thread_list_enumerate(self.build_tvshow_content, self.list, self.max_threads))
		[i.join() for i in threads]
		self.items.sort(key=lambda k: int(k[1].getProperty('david_sort_order')))
		return self.items

	def add_dir(self, url_params, mode='next_page', list_name=nextpage_str, iconImage=item_next, isFolder=True):
		url = build_url(url_params)
		listitem = make_listitem()
		listitem.setLabel(list_name)
		set_property = listitem.setProperty
		listitem.setArt({'icon': iconImage, 'fanart': fanart_empty})
		if mode == 'navigate_to_page': set_property('SpecialSort', 'top')
		else: set_property('SpecialSort', 'bottom')
		add_item(self.handle, url, listitem, isFolder)
