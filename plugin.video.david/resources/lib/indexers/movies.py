# -*- coding: utf-8 -*-
from metadata import movie_meta
from modules import kodi_utils, settings
from modules.meta_lists import oscar_winners
from modules.utils import manual_function_import, get_datetime, make_thread_list_enumerate
from modules.watched_status import get_watched_info_movie, get_watched_status_movie, get_bookmarks, get_progress_percent
# logger = kodi_utils.logger

meta_function, get_datetime_function, add_item, select_dialog = movie_meta, get_datetime, kodi_utils.add_item, kodi_utils.select_dialog
progress_percent_function, get_watched_function, get_watched_info_function = get_progress_percent, get_watched_status_movie, get_watched_info_movie
set_content, end_directory, set_view_mode, get_infolabel = kodi_utils.set_content, kodi_utils.end_directory, kodi_utils.set_view_mode, kodi_utils.get_infolabel
string, ls, sys, external_browse, add_items = str, kodi_utils.local_string, kodi_utils.sys, kodi_utils.external_browse, kodi_utils.add_items
make_listitem, build_url, remove_meta_keys, dict_removals = kodi_utils.make_listitem, kodi_utils.build_url, kodi_utils.remove_meta_keys, kodi_utils.movie_dict_removals
item_jump, item_next, poster_empty, fanart_empty = kodi_utils.item_jump, kodi_utils.item_next, kodi_utils.empty_poster, kodi_utils.addon_fanart
metadata_user_info, watched_indicators = settings.metadata_user_info, settings.watched_indicators
sleep, extras_open_action, get_art_provider, get_resolution = kodi_utils.sleep, settings.extras_open_action, settings.get_art_provider, settings.get_resolution
max_threads, widget_hide_next_page = settings.max_threads, settings.widget_hide_next_page
david_str, trakt_str, watched_str, unwatched_str, extras_str, options_str = ls(32036), ls(32037), ls(32642), ls(32643), ls(32645), ls(32646)
hide_str, exit_str, clearprog_str, nextpage_str, jumpto_str, play_str = ls(32648), ls(32649), ls(32651), ls(32799), ls(32964), '[B]%s...[/B]' % ls(32174)
addmenu_str, addshortcut_str = ls(32730), ls(32731)
run_plugin, container_refresh, container_update = 'RunPlugin(%s)', 'Container.Refresh(%s)', 'Container.Update(%s)'
tmdb_main = ('tmdb_movies_popular','tmdb_movies_blockbusters','tmdb_movies_in_theaters', 'tmdb_movies_upcoming', 'tmdb_movies_latest_releases', 'tmdb_movies_premieres')
trakt_main = ('trakt_movies_trending', 'trakt_movies_most_watched', 'trakt_movies_top10_boxoffice', 'trakt_recommendations')
trakt_personal = ('trakt_collection', 'trakt_watchlist', 'trakt_collection_lists')
imdb_personal  = ('imdb_watchlist', 'imdb_user_list_contents', 'imdb_keywords_list_contents')
tmdb_special_dict = {'tmdb_movies_languages': 'language', 'tmdb_movies_networks': 'company', 'tmdb_movies_year': 'year', 'tmdb_movies_certifications': 'certification',
					'tmdb_movies_recommendations': 'tmdb_id', 'tmdb_movies_genres': 'genre_id', 'tmdb_movies_search': 'query'}
personal_dict = {'in_progress_movies': ('modules.watched_status', 'get_in_progress_movies'), 'favorites_movies': ('modules.favorites', 'retrieve_favorites'),
				'watched_movies': ('modules.watched_status', 'get_watched_items'), 'recent_watched_movies': ('modules.watched_status', 'get_recently_watched')}

class Movies:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.id_type, self.list, self.action = self.params_get('id_type', 'tmdb_id'), self.params_get('list', []), self.params_get('action', None)
		self.items, self.new_page, self.total_pages, self.is_widget, self.max_threads = [], {}, None, external_browse(), max_threads()
		self.append = self.items.append

	def fetch_list(self):
		try:
			self.handle, self.builder, view_mode, content_type, mode = int(sys.argv[1]), self.worker, 'view.movies', 'movies', self.params_get('mode')
			try: page_no = int(self.params_get('new_page', '1'))
			except ValueError: page_no = self.params_get('new_page')
			if self.action in personal_dict: var_module, import_function = personal_dict[self.action]
			else: var_module, import_function = 'apis.%s_api' % self.action.split('_')[0], self.action
			try: function = manual_function_import(var_module, import_function)
			except: pass
			if self.action in tmdb_main:
				data = function(page_no)
				self.list = [i['id'] for i in data['results']]
				self.new_page = {'new_page': string(data['page'] + 1)}
			elif self.action in tmdb_special_dict:
				key = tmdb_special_dict[self.action]
				function_var = self.params_get(key, None)
				if not function_var: return
				data = function(function_var, page_no)
				self.list = [i['id'] for i in data['results']]
				if data['total_pages'] > page_no: self.new_page = {'new_page': string(data['page'] + 1), key: function_var}
			elif self.action in personal_dict:
				data, total_pages = function('movie', page_no)
				self.list = [i['media_id'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				if total_pages > page_no: self.new_page = {'new_page': string(page_no + 1)}
			elif self.action in trakt_main:
				self.id_type = 'trakt_dict'
				data = function(page_no)
				try: self.list = [i['movie']['ids'] for i in data]
				except: self.list = [i['ids'] for i in data]
				if self.action not in ('trakt_movies_top10_boxoffice', 'trakt_recommendations'): self.new_page = {'new_page': string(page_no + 1)}
			elif self.action in trakt_personal:
				self.id_type = 'trakt_dict'
				data, total_pages = function('movies', page_no)
				self.list = [i['media_ids'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				try:
					if total_pages > page_no: self.new_page = {'new_page': string(page_no + 1)}
				except: pass
			elif self.action in imdb_personal:
				self.id_type = 'imdb_id'
				list_id = self.params_get('list_id', None)
				data, next_page = function('movie', list_id, page_no)
				self.list = [i['imdb_id'] for i in data]
				if next_page: self.new_page = {'list_id': list_id, 'new_page': string(page_no + 1)}
			elif self.action == 'tmdb_movies_discover':
				name, query = self.params_get('name'), self.params_get('query')
				if page_no == 1:
					from indexers.discover import set_history
					set_history('movie', name, query)
				data = function(query, page_no)
				self.list = [i['id'] for i in data['results']]
				if data['total_pages'] > page_no: self.new_page = {'query': query, 'name': name, 'new_page': string(data['page'] + 1)}
			elif self.action  == 'tmdb_movies_search_collections':
				self.builder, view_mode, content_type = self.build_collections_results, 'view.main', ''
				query = self.params_get('query')
				data = function(query, page_no)
				self.list = data['results']
				if data['total_pages'] > page_no: self.new_page = {'new_page': string(page_no + 1), 'query': query}
			elif self.action  == 'tmdb_movies_collection':
				data = sorted(function(self.params_get('collection_id'))['parts'], key=lambda k: k['release_date'] or '2050')
				self.list = [i['id'] for i in data]
			elif self.action == 'imdb_movies_oscar_winners':
				self.list = oscar_winners[page_no-1]
				if len(oscar_winners) > page_no: self.new_page = {'new_page': string(page_no + 1)}
			if self.total_pages and not self.is_widget:
				url_params = {'mode': 'build_navigate_to_page', 'media_type': 'Movies', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode,
							'transfer_action': self.action, 'query': self.params_get('search_name', ''), 'actor_id': self.params_get('actor_id', '')}
				self.add_dir(url_params, 'navigate_to_page', jumpto_str, item_jump, False)
			add_items(self.handle, self.builder())
			if self.new_page and not self.widget_hide_next_page:
				self.new_page.update({'mode': mode, 'action': self.action, 'exit_list_params': self.exit_list_params})
				self.add_dir(self.new_page)
		except: pass
		set_content(self.handle, content_type)
		end_directory(self.handle, False if self.is_widget else None)
		if not self.is_widget: set_view_mode(view_mode, content_type)

	def build_movie_content(self, item_position, _id):
		try:
			cm = []
			cm_append = cm.append
			meta, playcount = self.get_meta(_id)
			meta_get = meta.get
			if meta_get('blank_entry', False): return
			listitem = make_listitem()
			set_properties = listitem.setProperties
			clearprog_params, unwatched_params, watched_params = '', '', ''
			title, year = meta_get('title'), meta_get('year')
			tmdb_id, imdb_id = meta_get('tmdb_id'), meta_get('imdb_id')
			poster = meta_get(self.poster_main) or meta_get(self.poster_backup) or poster_empty
			fanart = meta_get(self.fanart_main) or meta_get(self.fanart_backup) or fanart_empty
			clearlogo = meta_get(self.clearlogo_main) or meta_get(self.clearlogo_backup) or ''
			progress = progress_percent_function(self.bookmarks, tmdb_id)
			if playcount:
				if self.widget_hide_watched: return
				watched_action, watchedstr = 'mark_as_unwatched', unwatched_str
			else: watched_action, watchedstr = 'mark_as_watched', watched_str
			watched_params = build_url({'mode': 'mark_as_watched_unwatched_movie', 'action': watched_action, 'tmdb_id': tmdb_id, 'title': title, 'year': year})
			play_params = build_url({'mode': 'play_media', 'media_type': 'movie', 'tmdb_id': tmdb_id})
			extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'movie', 'is_widget': self.is_widget})
			options_params = build_url({'mode': 'options_menu_choice', 'content': 'movie', 'tmdb_id': tmdb_id, 'poster': poster, 'is_widget': self.is_widget})
			if self.fanart_enabled:
				banner, clearart, landscape, discart = meta_get('banner'), meta_get('clearart'), meta_get('landscape'), meta_get('discart')
			else: banner, clearart, landscape, discart = '', '', '', ''
			if self.open_extras:
				url_params = extras_params
				cm_append((play_str, run_plugin % play_params))
			else:
				url_params = play_params
				cm_append((extras_str, run_plugin % extras_params))
			cm_append((options_str, run_plugin % options_params))
			if progress:
				clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'media_type': 'movie', 'tmdb_id': tmdb_id, 'refresh': 'true'})
				set_properties({'WatchedProgress': progress, 'resumetime': progress, 'david_in_progress': 'true'})
				cm_append((clearprog_str, run_plugin % clearprog_params))
			cm_append((watchedstr % self.watched_title, run_plugin % watched_params))
			cm_append((exit_str, container_refresh % self.exit_list_params))
			listitem.setLabel(title)
			listitem.addContextMenuItems(cm)
			listitem.setCast(meta_get('cast', []))
			listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id)})
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart,
							'clearlogo': clearlogo, 'landscape': landscape, 'discart': discart})
			listitem.setInfo('Video', remove_meta_keys(meta, dict_removals))
			set_properties({'david_widget': 'false', 'david_sort_order': string(item_position)})
			if self.is_widget:
				set_properties({'david_widget': 'true', 'david_playcount': string(playcount), 'david_extras_params': extras_params,'david_options_params': options_params,
								'david_unwatched_params': unwatched_params, 'david_watched_params': watched_params, 'david_clearprog_params': clearprog_params})
			self.append((url_params, listitem, False))
		except: pass

	def get_meta(self, _id):
		meta = meta_function(self.id_type, _id, self.meta_user_info, self.current_date)
		if not meta: return
		playcount, overlay = get_watched_function(self.watched_info, string(meta['tmdb_id']))
		meta.update({'playcount': playcount, 'overlay': overlay})
		return meta, playcount

	def worker(self):
		self.exit_list_params = self.params_get('exit_list_params', None) or get_infolabel('Container.FolderPath')
		self.current_date = get_datetime_function()
		self.meta_user_info = metadata_user_info()
		self.watched_indicators = watched_indicators()
		self.watched_info = get_watched_info_function(self.watched_indicators)
		self.bookmarks = get_bookmarks(self.watched_indicators, 'movie')
		self.open_extras = extras_open_action('movie')
		self.fanart_enabled = self.meta_user_info['extra_fanart_enabled']
		self.widget_hide_next_page = False if not self.is_widget else widget_hide_next_page()
		self.widget_hide_watched = self.is_widget and self.meta_user_info['widget_hide_watched']
		self.watched_title = trakt_str if self.watched_indicators == 1 else david_str
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup, self.clearlogo_main, self.clearlogo_backup = get_art_provider()
		threads = list(make_thread_list_enumerate(self.build_movie_content, self.list, self.max_threads))
		[i.join() for i in threads]
		self.items.sort(key=lambda k: int(k[1].getProperty('david_sort_order')))
		return self.items

	def build_collections_results(self):
		def _process(item_position, item):
			cm = []
			cm_append = cm.append
			name, poster_path, backdrop_path = item['name'], item['poster_path'], item['backdrop_path']
			if poster_path: poster = tmdb_image_url % (poster_res, poster_path)
			else: poster = poster_empty
			if backdrop_path: fanart = tmdb_image_url % (fanart_res, backdrop_path)
			else: fanart = fanart_empty
			url_params = build_url({'mode': 'build_movie_list', 'action': 'tmdb_movies_collection', 'collection_id':item['id'] })
			listitem = make_listitem()
			listitem.setLabel(name)
			listitem.setInfo('Video', {'plot': item['overview']})
			listitem.setArt({'icon': poster, 'fanart': fanart})
			cm_append((addmenu_str, run_plugin % build_url({'mode': 'menu_editor.add_external', 'name': name, 'iconImage': poster})))
			cm_append((addshortcut_str, run_plugin % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': name, 'iconImage': poster})))
			listitem.addContextMenuItems(cm)
			listitem.setProperty('david_sort_order', string(item_position))
			self.append((url_params, listitem, True))
		image_resolution = get_resolution()
		poster_res, fanart_res = image_resolution['poster'], image_resolution['fanart']
		tmdb_image_url = 'https://image.tmdb.org/t/p/%s%s'
		threads = list(make_thread_list_enumerate(_process, self.list, self.max_threads))
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
