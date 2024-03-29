# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from windows import BaseDialog
from apis import tmdb_api, imdb_api
from indexers import dialogs, people
from indexers.images import Images
from modules import kodi_utils, watched_status, settings, episode_tools
from modules.sources import Sources
from modules.downloader import runner
from modules.utils import get_datetime
from modules.meta_lists import networks
# logger = kodi_utils.logger

json, Thread, get_icon, close_all_dialog, ok_dialog = kodi_utils.json, kodi_utils.Thread, kodi_utils.get_icon, kodi_utils.close_all_dialog, kodi_utils.ok_dialog
fetch_kodi_imagecache, addon_fanart, empty_poster = kodi_utils.fetch_kodi_imagecache, kodi_utils.addon_fanart, kodi_utils.empty_poster
addon_icon, ls, get_icon = kodi_utils.addon_icon, kodi_utils.local_string, kodi_utils.get_icon
backup_cast_thumbnail = get_icon('genre_family')
tmdb_image_base = 'https://image.tmdb.org/t/p/%s%s'
count_insert = '%02d'
button_ids = (10, 11, 12, 13, 14, 15, 16, 17, 50)
cast_id, recommended_id, reviews_id, trivia_id, blunders_id, parentsguide_id = 2050, 2051, 2052, 2053, 2054, 2055
videos_id, posters_id, backdrops_id, year_id, genres_id, networks_id, collection_id = 2056, 2057, 2058, 2059, 2060, 2061, 2062
playbrowse_id, trailer_id, keywords_id, images_id, extrainfo_id, genre_id, directorrandom_id, optons_id, plot_id = button_ids
tmdb_list_ids = (recommended_id, year_id, genres_id, networks_id, collection_id)
imdb_list_ids = (reviews_id, trivia_id, blunders_id, parentsguide_id)
art_ids = (posters_id, backdrops_id)
parentsguide_levels = {'mild': ls(32996), 'moderate': ls(32997), 'severe': ls(32998), 'none': 'No Rank'}
parentsguide_inputs = {'Sex & Nudity': (ls(32990), get_icon('sex_nudity')), 'Violence & Gore': (ls(32991), get_icon('genre_war')), 'Profanity': (ls(32992), get_icon('bad_language')),
						'Alcohol, Drugs & Smoking': (ls(32993), get_icon('drugs_alcohol')), 'Frightening & Intense Scenes': (ls(32994), get_icon('genre_horror'))}

class Extras(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.control_id = None
		self.set_starting_constants(kwargs)
		self.set_properties()

	def onInit(self):
		tasks = (self.set_poster, self.make_cast, self.make_recommended, self.make_reviews, self.make_trivia, self.make_blunders,
				self.make_parentsguide, self.make_videos, self.make_year, self.make_genres, self.make_network)
		[Thread(target=i).start() for i in tasks]
		for i in ('posters', 'backdrops'): Thread(target=self.make_artwork, args=(i,)).start()
		if self.media_type == 'movie': Thread(target=self.make_collection).start()
		else: self.setProperty('extras.make.collection', 'false')

	def run(self):
		self.doModal()
		self.clearProperties()
		if self.selected: self.execute_code(self.selected)

	def onClick(self, controlID):
		self.control_id = None
		if controlID in button_ids:
			if controlID == playbrowse_id:
				if self.media_type == 'movie':
					url_params = {'mode': 'play_media', 'media_type': 'movie', 'tmdb_id': self.tmdb_id}
					Sources().playback_prep(url_params)
				else:
					close_all_dialog()
					url_params = self.make_tvshow_browse_params()
					self.selected = self.folder_runner % self.build_url(url_params)
					self.close()
			elif controlID == trailer_id:
				chosen = dialogs.trailer_choice(self.media_type, self.poster, self.tmdb_id, self.meta['trailer'], self.meta['all_trailers'])
				if not chosen: return ok_dialog()
				elif chosen == 'canceled': return
				self.open_window(('windows.videoplayer', 'VideoPlayer'), 'videoplayer.xml', video=chosen)
			elif controlID == keywords_id:
				base_media = 'movies' if self.media_type == 'movie' else 'tv'
				keyword_params = dialogs.imdb_keywords_choice(base_media, self.imdb_id, self.poster)
				if not keyword_params: return
				close_all_dialog()
				self.selected = self.folder_runner % self.build_url(keyword_params)
				self.close()
			elif controlID == images_id:
				Images().run({'mode': 'imdb_image_results', 'imdb_id': self.imdb_id, 'media_title': self.rootname, 'page_no': 1, 'rolling_count_list': [0]})
			elif controlID == extrainfo_id:
				text = dialogs.media_extra_info(self.media_type, self.meta)
				return self.show_text_media(text)
			elif controlID == genre_id:
				if not self.genre: return
				base_media = 'movies' if self.media_type == 'movie' else 'tv'
				genre_params = dialogs.genres_choice(base_media, self.genre, self.poster)
				if not genre_params: return
				close_all_dialog()
				self.selected = self.folder_runner % self.build_url(genre_params)
				self.close()
			elif controlID == directorrandom_id:
				if self.media_type == 'movie':
					director = self.meta.get('director', None)
					if not director: return
					return people.person_data_dialog({'query': director})
				else:
					function = dialogs.random_choice({'tmdb_id': self.tmdb_id, 'poster': self.poster, 'return_choice': 'true', 'window_xml': 'media_select.xml'})
					if not function: return
					exec('episode_tools.%s(self.tmdb_id)' % function)
					self.close()
			elif controlID == optons_id:
				params = {'content': self.media_type, 'tmdb_id': self.tmdb_id, 'poster': self.poster, 'is_widget': self.is_widget, 'window_xml': 'media_select.xml'}
				return dialogs.options_menu(params, self.meta)
			elif controlID == plot_id:
				return self.show_text_media(self.plot)
		else: self.control_id = controlID

	def onAction(self, action):
		if action in self.closing_actions: return self.close()
		if action in self.context_actions:
			focus_id = self.getFocusId()
			if focus_id in (posters_id, backdrops_id):
				chosen_listitem = self.get_listitem(focus_id)
				image = chosen_listitem.getProperty('extras.thumbnail')
				params = {'action': 'image', 'name': '%s %s' % (self.rootname, chosen_listitem.getProperty('extras.name')),
						'thumb_url': image.replace('w780', {posters_id: 'w185', backdrops_id: 'w300'}[focus_id]), 'image_url': image.replace('w780', 'original'),
						'media_type': 'image', 'image': addon_icon}
				return runner(params)
			elif focus_id == cast_id:
				person_name = self.get_listitem(focus_id).getProperty(self.item_action_dict[focus_id])
				return people.person_search(person_name, window_xml='media_select.xml')
			else: return
		if not self.control_id: return
		if action in self.selection_actions:
			try: chosen_var = self.get_listitem(self.control_id).getProperty(self.item_action_dict[self.control_id])
			except: return
			if self.control_id == cast_id:
				return people.person_data_dialog({'query': chosen_var})
			elif self.control_id in tmdb_list_ids:
				params = {'tmdb_id': chosen_var, 'media_type': self.media_type}
				return dialogs.extras_menu(params)
			elif self.control_id in imdb_list_ids:
				if self.control_id == parentsguide_id:
					if not chosen_var: return
					self.show_text_media(chosen_var)
				else:
					end_index = self.show_text_media_list(chosen_var)
					self.getControl(self.control_id).selectItem(end_index)
			elif self.control_id in art_ids:
				end_index = Images().run({'mode': 'slideshow_image', 'all_images': getattr(self, chosen_var), 'current_index': self.get_position(self.control_id)})
				self.getControl(self.control_id).selectItem(end_index)
			elif self.control_id == videos_id:
				chosen = dialogs.imdb_videos_choice(getattr(self, chosen_var)[self.get_position(self.control_id)]['videos'], self.poster)
				if not chosen: return
				self.open_window(('windows.videoplayer', 'VideoPlayer'), 'videoplayer.xml', meta=self.meta, video=chosen)
			else: return

	def make_cast(self):
		if not cast_id in self.enabled_lists: return
		def builder():
			for item in self.meta['cast']:
				try:
					listitem = self.make_listitem()
					thumbnail = item['thumbnail'] or backup_cast_thumbnail
					listitem.setProperty('extras.name', item['name'])
					listitem.setProperty('extras.role', item['role'])
					listitem.setProperty('extras.thumbnail', thumbnail)
					yield listitem
				except: pass
		try:
			item_list = list(builder())
			self.setProperty('extras.cast.number', count_insert % len(item_list))
			self.item_action_dict[cast_id] = 'extras.name'
			self.add_items(cast_id, item_list)
		except: pass

	def make_recommended(self):
		if not recommended_id in self.enabled_lists: return
		try:
			function = tmdb_api.tmdb_movies_recommendations if self.media_type == 'movie' else tmdb_api.tmdb_tv_recommendations
			data = function(self.tmdb_id, 1)['results']
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('extras.recommended.number', count_insert % len(item_list))
			self.item_action_dict[recommended_id] = 'extras.tmdb_id'
			self.add_items(recommended_id, item_list)
		except: pass

	def make_reviews(self):
		if not reviews_id in self.enabled_lists: return
		def builder():
			for item in self.all_reviews:
				try:
					listitem = self.make_listitem()
					listitem.setProperty('extras.text', item)
					listitem.setProperty('extras.content_list', 'all_reviews')
					yield listitem
				except: pass
		try:
			self.all_reviews = imdb_api.imdb_reviews(self.imdb_id)
			item_list = list(builder())
			self.setProperty('extras.imdb_reviews.number', count_insert % len(item_list))
			self.item_action_dict[reviews_id] = 'extras.content_list'
			self.add_items(reviews_id, item_list)
		except: pass

	def make_trivia(self):
		if not trivia_id in self.enabled_lists: return
		def builder():
			for item in self.all_trivia:
				try:
					listitem = self.make_listitem()
					listitem.setProperty('extras.text', item)
					listitem.setProperty('extras.content_list', 'all_trivia')
					yield listitem
				except: pass
		try:
			self.all_trivia = imdb_api.imdb_trivia(self.imdb_id)
			item_list = list(builder())
			self.setProperty('extras.imdb_trivia.number', count_insert % len(item_list))
			self.item_action_dict[trivia_id] = 'extras.content_list'
			self.add_items(trivia_id, item_list)
		except: pass

	def make_blunders(self):
		if not blunders_id in self.enabled_lists: return
		def builder():
			for item in self.all_blunders:
				try:
					listitem = self.make_listitem()
					listitem.setProperty('extras.text', item)
					listitem.setProperty('extras.content_list', 'all_blunders')
					yield listitem
				except: pass
		try:
			self.all_blunders = imdb_api.imdb_blunders(self.imdb_id)
			item_list = list(builder())
			self.setProperty('extras.imdb_blunders.number', count_insert % len(item_list))
			self.item_action_dict[blunders_id] = 'extras.content_list'
			self.add_items(blunders_id, item_list)
		except: pass

	def make_parentsguide(self):
		if not parentsguide_id in self.enabled_lists: return
		def builder():
			for item in data:
				try:
					listitem = self.make_listitem()
					name = parentsguide_inputs[item['title']][0]
					ranking = parentsguide_levels[item['ranking'].lower()].upper()
					if item['content']: ranking += ' (x%02d)' % item['total_count']
					icon = parentsguide_inputs[item['title']][1]
					listitem.setProperty('extras.name', name)
					listitem.setProperty('extras.ranking', ranking)
					listitem.setProperty('extras.thumbnail', icon)
					listitem.setProperty('extras.content', item['content'])
					yield listitem
				except: pass
		try:
			data = imdb_api.imdb_parentsguide(self.imdb_id)
			item_list = list(builder())
			self.setProperty('extras.imdb_parentsguide.number', count_insert % len(item_list))
			self.item_action_dict[parentsguide_id] = 'extras.content'
			self.add_items(parentsguide_id, item_list)
		except: pass

	def make_videos(self):
		if not videos_id in self.enabled_lists: return
		def builder():
			for item in self.all_videos:
				try:
					listitem = self.make_listitem()
					listitem.setProperty('extras.name', item['title'])
					listitem.setProperty('extras.thumbnail', item['poster'])
					listitem.setProperty('extras.content_list', 'all_videos')
					yield listitem
				except: pass
		try:
			self.all_videos = imdb_api.imdb_videos(self.imdb_id)
			item_list = list(builder())
			self.setProperty('extras.imdb_videos.number', count_insert % len(item_list))
			self.item_action_dict[videos_id] = 'extras.content_list'
			self.add_items(videos_id, item_list)
		except: pass

	def make_artwork(self, image_type):
		tmdb_image_list = []
		if image_type == 'posters':
			if not posters_id in self.enabled_lists: return
			_id, resolution, art_list_id, self.tmdb_posters, used_image, default_image = posters_id, 'w342', 'tmdb_posters', tmdb_image_list, self.poster, empty_poster
		else:
			if not backdrops_id in self.enabled_lists: return
			_id, resolution, art_list_id, self.tmdb_backdrops, used_image, default_image = backdrops_id, 'w780', 'tmdb_backdrops', tmdb_image_list, self.fanart, addon_fanart
		def builder():
			for count, item in enumerate(data, 1):
				try:
					listitem = self.make_listitem()
					thumb_url = tmdb_image_base % (resolution, item['file_path'])
					try: name = '%sx%s' % (item['height'], item['width'])
					except: name = 'Default'
					listitem.setProperty('extras.name', '%01d. %s' % (count, name))
					listitem.setProperty('extras.thumbnail', thumb_url)
					listitem.setProperty('extras.all_images', art_list_id)
					yield listitem
				except: pass
		try:
			dbtype = 'movie' if self.media_type == 'movie' else 'tv'
			try: data = self.meta['images'][image_type]
			except: data = tmdb_api.tmdb_media_images(dbtype, self.tmdb_id)[image_type]
			tmdb_image_list.extend([(tmdb_image_base % ('original', i['file_path']), '%sx%s' % (i['height'], i['width'])) for i in data])
			if used_image != default_image:
				try:
					used_image = '/%s' % used_image.split('/')[-1]
					if not any(i['file_path'] == used_image for i in data):
						default_data = {'file_path': used_image}
						data.append(default_data)
						tmdb_image_list.append((tmdb_image_base % ('original', default_data['file_path']), 'Default'))
				except: pass
			item_list = list(builder())
			self.setProperty('extras.tmdb_artwork.%s.number' % image_type, count_insert % len(item_list))
			self.item_action_dict[_id] = 'extras.all_images'
			self.add_items(_id, item_list)
		except: pass

	def make_year(self):
		if not year_id in self.enabled_lists: return
		try:
			function = tmdb_api.tmdb_movies_year if self.media_type == 'movie' else tmdb_api.tmdb_tv_year
			data = self.remove_current_tmdb_mediaitem(function(self.year, 1)['results'])
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('extras.more_from_year.number', count_insert % len(item_list))
			self.item_action_dict[year_id] = 'extras.tmdb_id'
			self.add_items(year_id, item_list)
		except: pass

	def make_genres(self):
		if not genres_id in self.enabled_lists: return
		try:
			function = tmdb_api.tmdb_movies_genres if self.media_type == 'movie' else tmdb_api.tmdb_tv_genres
			genre_dict = dialogs.genres_choice(self.media_type, self.genre, '', return_genres=True)
			genre_list = ','.join([i['value'][0] for i in genre_dict])
			data = self.remove_current_tmdb_mediaitem(function(genre_list, 1)['results'])
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('extras.more_from_genres.number', count_insert % len(item_list))
			self.item_action_dict[genres_id] = 'extras.tmdb_id'
			self.add_items(genres_id, item_list)
		except: pass

	def make_network(self):
		if not networks_id in self.enabled_lists: return
		try:
			network = self.meta['studio']
			network_id = [i['id'] for i in tmdb_api.tmdb_company_id(network)['results'] if i['name'] == network][0] \
						if self.media_type == 'movie' else [item['id'] for item in networks if 'name' in item and item['name'] == network][0]
			function = tmdb_api.tmdb_movies_networks if self.media_type == 'movie' else tmdb_api.tmdb_tv_networks
			data = self.remove_current_tmdb_mediaitem(function(network_id, 1)['results'])
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('extras.more_from_networks.number', count_insert % len(item_list))
			self.item_action_dict[networks_id] = 'extras.tmdb_id'
			self.add_items(networks_id, item_list)
		except: pass

	def make_collection(self):
		if not collection_id in self.enabled_lists: return
		try: coll_id = self.meta['extra_info']['collection_id']
		except: return
		if not coll_id: return
		try:
			data = tmdb_api.tmdb_movies_collection(coll_id)
			poster_path = data['poster_path']
			if poster_path: poster = tmdb_image_base % (self.poster_resolution, poster_path)
			else: poster = empty_poster
			item_list = list(self.make_tmdb_listitems(sorted(data['parts'], key=lambda k: k['release_date'] or '2050')))
			self.setProperty('extras.more_from_collection.name', data['name'])
			self.setProperty('extras.more_from_collection.overview', data['overview'])
			self.setProperty('extras.more_from_collection.poster', poster)
			self.setProperty('extras.more_from_collection.number', count_insert % len(item_list))
			self.item_action_dict[collection_id] = 'extras.tmdb_id'
			self.add_items(collection_id, item_list)
		except: pass

	def get_release_year(self, release_data):
		try:
			if release_data in ('', None): release_data = 'N/A'
			else: release_data = release_data.split('-')[0]
		except: pass
		return release_data

	def get_finish(self):
		if self.percent_watched in ('0', '100') and self.listitem_check():
			finished = self.get_infolabel('ListItem.EndTime')
		else:
			kodi_clock = self.get_infolabel('System.Time')
			if any(i in kodi_clock for i in ['AM', 'PM']): _format = '%I:%M %p'
			else: _format = '%H:%M'
			current_time = datetime.now()
			remaining_time = ((100 - int(self.percent_watched))/100) * self.duration_data
			finish_time = current_time + timedelta(minutes=remaining_time)
			finished = finish_time.strftime(_format)
		return '%s: %s' % (ls(33062), finished)

	def get_duration(self):
		return ls(33058) % self.duration_data

	def get_progress(self):
		self.percent_watched = watched_status.get_progress_percent(watched_status.get_bookmarks(self.watched_indicators, 'movie'), self.tmdb_id)
		if not self.percent_watched:
			try:
				watched_info = watched_status.get_watched_info_movie(self.watched_indicators)
				self.percent_watched = '100' if watched_status.get_watched_status_movie(watched_info, str(self.tmdb_id))[0] == 1 else '0'
			except: self.percent_watched = '0'
		progress_status = '%s%% %s' % (self.percent_watched, ls(32475))
		return progress_status

	def get_last_aired(self):
		extra_info = self.meta['extra_info']
		if extra_info.get('last_episode_to_air', False):
			last_ep = extra_info['last_episode_to_air']
			last_aired = 'S%.2dE%.2d' % (last_ep['season_number'], last_ep['episode_number'])
		else: return ''
		return '%s: %s' % (ls(32634), last_aired)

	def get_next_aired(self):
		extra_info = self.meta['extra_info']
		if extra_info.get('next_episode_to_air', False):
			next_ep = extra_info['next_episode_to_air']
			next_aired = 'S%.2dE%.2d' % (next_ep['season_number'], next_ep['episode_number'])
		else: return ''
		return '%s: %s' % (ls(32635), next_aired)

	def get_next_episode(self):
		watched_info = watched_status.get_watched_info_tv(self.watched_indicators)
		ep_list = watched_status.get_next_episodes(watched_info)
		try: info = [i for i in ep_list if i['media_ids']['tmdb'] == self.tmdb_id][0]
		except: return ''
		current_season = info['season']
		current_episode = info['episode']
		season_data = self.meta['season_data']
		curr_season_data = [i for i in season_data if i['season_number'] == current_season][0]
		season = current_season if current_episode < curr_season_data['episode_count'] else current_season + 1
		episode = current_episode + 1 if current_episode < curr_season_data['episode_count'] else 1
		try: info = [i for i in season_data if i['season_number'] == season][0]
		except: return ''
		if info['episode_count'] >= episode:
			next_episode = 'S%.2dE%.2d' % (season, episode)
			return '%s: %s' % (ls(33041), next_episode)
		else: return ''

	def make_tvshow_browse_params(self):
		total_seasons = self.meta['total_seasons']
		all_episodes = settings.default_all_episodes()
		show_all_episodes = True if all_episodes in (1, 2) else False
		if show_all_episodes:
			if all_episodes == 1 and total_seasons > 1: url_params = {'mode': 'build_season_list', 'tmdb_id': self.tmdb_id}
			else: url_params = {'mode': 'build_episode_list', 'tmdb_id': self.tmdb_id, 'season': 'all'}
		else: url_params = {'mode': 'build_season_list', 'tmdb_id': self.tmdb_id}
		return url_params

	def original_poster(self):
		poster = self.meta.get(self.poster_main) or self.meta.get(self.poster_backup) or empty_poster
		self.current_poster = poster
		if 'image.tmdb' in self.current_poster:
			try: poster = self.current_poster.replace('w185', 'original').replace('w342', 'original').replace('w780', 'original')
			except: pass
		elif 'fanart.tv' in self.current_poster:
			if not self.check_poster_cached(self.current_poster): self.current_poster = self.meta.get(self.poster_backup) or empty_poster
		return poster

	def original_fanart(self):
		fanart = self.meta.get(self.fanart_main) or self.meta.get(self.fanart_backup) or addon_fanart
		return fanart

	def remove_current_tmdb_mediaitem(self, data):
		return [i for i in data if int(i['id']) != self.tmdb_id]

	def make_tmdb_listitems(self, data):
		name_key = 'title' if self.media_type == 'movie' else 'name'
		release_key = 'release_date' if self.media_type == 'movie' else 'first_air_date'
		for item in data:
			try:
				listitem = self.make_listitem()
				poster_path = item['poster_path']
				if poster_path: thumbnail = tmdb_image_base % (self.poster_resolution, poster_path)
				else: thumbnail = empty_poster
				year = self.get_release_year(item[release_key])
				listitem.setProperty('extras.name', item[name_key])
				listitem.setProperty('extras.release_date', year)
				listitem.setProperty('extras.vote_average', '%.1f' % item['vote_average'])
				listitem.setProperty('extras.thumbnail', thumbnail)
				listitem.setProperty('extras.tmdb_id', str(item['id']))
				yield listitem
			except: pass

	def listitem_check(self):
		return self.get_infolabel('ListItem.Title') == self.meta['title']

	def add_items(self,_id, items):
		self.getControl(_id).addItems(items)

	def set_poster(self):
		if self.current_poster:
			self.getControl(200).setImage(self.current_poster)
			self.getControl(201).setImage(self.poster)
			total_time = 0
			while not self.check_poster_cached(self.poster):
				if total_time >= 200: break
				total_time += 1
				self.sleep(50)
			self.getControl(200).setImage(self.poster)
		else: self.setProperty('extras.active_poster', 'false')

	def check_poster_cached(self, poster):
		try:
			if poster == empty_poster: return True
			if fetch_kodi_imagecache(poster): return True
			return False
		except: return True

	def show_text_media(self, text):
		return self.open_window(('windows.extras', 'ShowTextMedia'), 'textviewer_media.xml', text=text, poster=self.poster)

	def show_text_media_list(self, chosen_var):
		return self.open_window(('windows.extras', 'ShowTextMedia'), 'textviewer_media_list.xml',
								items=getattr(self, chosen_var), current_index=self.get_position(self.control_id), poster=self.poster)

	def set_starting_constants(self, kwargs):
		self.item_action_dict = {}
		self.selected = None
		self.meta = kwargs['meta']
		self.media_type = self.meta['mediatype']#movie, tvshow
		self.tmdb_id = self.meta['tmdb_id']
		self.imdb_id = self.meta['imdb_id']
		self.is_widget = kwargs['is_widget'].lower()
		if self.is_widget == 'true': self.folder_runner = 'ActivateWindow(Videos,%s,return)'
		else: self.folder_runner = 'Container.Update(%s)'
		self.enabled_lists = settings.extras_enabled_menus()
		self.enable_scrollbars = settings.extras_enable_scrollbars()
		self.enable_animation = settings.extras_enable_animation()
		self.poster_resolution = settings.get_resolution()['poster']
		self.watched_indicators = settings.watched_indicators()
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup, self.clearlogo_main, self.clearlogo_backup = settings.get_art_provider()
		self.title = self.meta['title']
		self.year = str(self.meta['year'])
		self.rootname = self.meta['rootname']
		self.poster = self.original_poster()
		self.fanart = self.original_fanart()
		self.clearlogo = self.meta.get(self.clearlogo_main) or self.meta.get(self.clearlogo_backup) or ''
		self.plot = self.meta['tvshow_plot'] if 'tvshow_plot' in self.meta else self.meta['plot']
		if not self.plot: self.plot = ''
		self.rating = str(self.meta['rating'])
		self.mpaa = self.meta['mpaa']
		self.status = self.meta['extra_info'].get('status', '').replace('Series', '')
		self.genre = self.meta['genre']
		self.network = self.meta['studio'] or 'N/A'
		if not self.network: self.network = ''
		self.duration_data = int(float(self.meta['duration'])/60)
		self.duration = self.get_duration()
		if self.media_type == 'movie':
			self.progress = self.get_progress()
			self.finish_watching = self.get_finish()
			self.last_aired_episode, self.next_aired_episode, self.next_episode = '', '', ''
		else:
			self.progress, self.finish_watching = '', ''
			self.last_aired_episode = self.get_last_aired()
			if self.status not in ('', 'Ended', 'Canceled'): self.next_aired_episode = self.get_next_aired()
			else: self.next_aired_episode = ''
			self.next_episode = self.get_next_episode()

	def set_properties(self):
		self.setProperty('extras.media_type', self.media_type)
		self.setProperty('extras.fanart', self.fanart)
		self.setProperty('extras.clearlogo', self.clearlogo)
		self.setProperty('extras.title', self.title)
		self.setProperty('extras.plot', self.plot)
		self.setProperty('extras.year', self.year)
		self.setProperty('extras.rating', self.rating)
		self.setProperty('extras.mpaa', self.mpaa)
		self.setProperty('extras.status', self.status)
		self.setProperty('extras.genre', self.genre)
		self.setProperty('extras.network', self.network)
		self.setProperty('extras.duration', self.duration)
		self.setProperty('extras.progress', self.progress)
		self.setProperty('extras.finish_watching', self.finish_watching)
		self.setProperty('extras.last_aired_episode', self.last_aired_episode)
		self.setProperty('extras.next_aired_episode', self.next_aired_episode)
		self.setProperty('extras.next_episode', self.next_episode)
		self.setProperty('extras.enable_scrollbars', self.enable_scrollbars)
		self.setProperty('extras.enable_animation', self.enable_animation)

class ShowTextMedia(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.poster = kwargs.get('poster')
		self.text = kwargs.get('text', None)
		self.items = kwargs.get('items', None)
		self.position = kwargs.get('current_index', None)
		if self.items: self.make_menu()
		self.window_id = 2060
		self.set_properties()

	def onInit(self):
		if self.items:
			self.win = self.getControl(self.window_id)
			self.win.addItems(self.item_list)
			self.win.selectItem(self.position)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		if self.items: return self.position

	def onAction(self, action):
		if action in self.closing_actions:
			if self.items: self.position = self.get_position(self.window_id)
			self.close()

	def make_menu(self):
		def builder():
			for item in self.items:
				listitem = self.make_listitem()
				listitem.setProperty('text_media.text', item)
				yield listitem
		self.item_list = list(builder())

	def set_properties(self):
		if not self.items: self.setProperty('text_media.text', self.text)
		self.setProperty('text_media.poster', self.poster)

class ExtrasChooser(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 5001
		self.kwargs = kwargs
		self.preselect = self.kwargs['preselect']
		self.items = json.loads(self.kwargs['items'])
		self.chosen_indexes = []
		self.append = self.chosen_indexes.append
		self.selected = None
		self.make_menu()

	def onInit(self):
		self.win = self.getControl(self.window_id)
		self.win.addItems(self.item_list)
		if self.preselect:
			for index in self.preselect:
				self.item_list[index].setProperty('check_status', 'checked')
				self.append(index)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		return self.selected

	def onClick(self, controlID):
		if controlID == 10:
			self.selected = sorted(self.chosen_indexes)
			self.close()
		elif controlID == 11:
			self.close()

	def onAction(self, action):
		if action in self.selection_actions:
			position = self.get_position(self.window_id)
			chosen_listitem = self.get_listitem(self.window_id)
			if chosen_listitem.getProperty('check_status') == 'checked':
				chosen_listitem.setProperty('check_status', '')
				self.chosen_indexes.remove(position)
			else:
				chosen_listitem.setProperty('check_status', 'checked')
				self.append(position)
		elif action in self.closing_actions:
			return self.close()

	def make_menu(self):
		def builder():
			for item in self.items:
				listitem = self.make_listitem()
				listitem.setProperty('extras_chooser.name', item['name'])
				listitem.setProperty('extras_chooser.image', item['image'])
				listitem.setProperty('extras_chooser.item', json.dumps(item))
				yield listitem
		self.item_list = list(builder())
