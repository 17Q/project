# -*- coding: utf-8 -*-
import re
import os
from apis.opensubtitles_api import OpenSubtitlesAPI
from apis.trakt_api import make_trakt_slug
from modules import kodi_utils as ku, settings as st, watched_status as ws
from modules.meta_lists import language_choices
from modules.utils import sec2time, clean_file_name
# logger = ku.logger

Thread, json, ls, xbmc_player, translate_path, execute_builtin, sleep = ku.Thread, ku.json, ku.local_string, ku.xbmc_player, ku.translate_path, ku.execute_builtin, ku.sleep
get_property, set_property, clear_property, convert_language, get_visibility = ku.get_property, ku.set_property, ku.clear_property, ku.convert_language, ku.get_visibility
make_listitem, volume_checker, list_dirs, get_setting, confirm_progress_media = ku.make_listitem, ku.volume_checker, ku.list_dirs, ku.get_setting, ku.confirm_progress_media
close_all_dialog, notification, select_dialog, poster_empty, fanart_empty, sys = ku.close_all_dialog, ku.notification, ku.select_dialog, ku.empty_poster, ku.addon_fanart, ku.sys
get_art_provider, get_fanart_data, watched_indicators, auto_resume = st.get_art_provider, st.get_fanart_data, st.watched_indicators, st.auto_resume
autoplay_next_episode, autoplay_next_settings = st.autoplay_next_episode, st.autoplay_next_settings
get_progress_percent, get_bookmarks, erase_bookmark, clear_local_bookmarks = ws.get_progress_percent, ws.get_bookmarks, ws.erase_bookmark, ws.clear_local_bookmarks
set_bookmark, mark_as_watched_unwatched_movie, mark_as_watched_unwatched_episode = ws.set_bookmark, ws.mark_as_watched_unwatched_movie, ws.mark_as_watched_unwatched_episode

class DavidPlayer(xbmc_player):
	def __init__ (self):
		xbmc_player.__init__(self)
		self.set_resume, self.set_watched = 5, 90
		self.media_marked, self.subs_searched, self.nextep_info_gathered = False, False, False
		self.nextep_started, self.random_continual_started = False, False
		self.autoplay_next_episode, self.play_random_continual = False, False
		self.failed_playback, self.return_value = False, True
		self.volume_check = get_setting('volumecheck.enabled', 'false') == 'true'
		self.disable_content_lookup = st.disable_content_lookup()
		self.check_successful_playback = st.playback_check_success()
		if self.check_successful_playback: self.max_count = st.playback_success_timeout()
		else: self.max_count = 300

	def run(self, url=None, obj=None):
		close_all_dialog()
		if not url: return False
		self.object = obj
		if self.volume_check: volume_checker(get_setting('volumecheck.percent', '100'))
		try:
			if self.object == 'video':
				listitem = make_listitem()
				listitem.setPath(url)
				listitem.setInfo('video', {'FileNameAndPath': url})
				if self.disable_content_lookup: listitem.setContentLookup(False)
				return self.play(url, listitem)
			self.meta = json.loads(get_property('david_playback_meta'))
			self.meta_get = self.meta.get
			self.tmdb_id, self.imdb_id, self.tvdb_id = self.meta_get('tmdb_id'), self.meta_get('imdb_id'), self.meta_get('tvdb_id')
			self.media_type, self.title, self.year = self.meta_get('media_type'), self.meta_get('title'), self.meta_get('year')
			self.season, self.episode = self.meta_get('season', ''), self.meta_get('episode', '')
			if 'random' in self.meta or 'random_continual' in self.meta: bookmark = 0
			else: bookmark = self.bookmark()
			if bookmark == 'cancel': return True
			self.meta.update({'url': url, 'bookmark': bookmark})
			try:
				poster_main, poster_backup, fanart_main, fanart_backup, clearlogo_main, clearlogo_backup = get_art_provider()
				poster = self.meta_get(poster_main) or self.meta_get(poster_backup) or poster_empty
				fanart = self.meta_get(fanart_main) or self.meta_get(fanart_backup) or fanart_empty
				clearlogo = self.meta_get(clearlogo_main) or self.meta_get(clearlogo_backup) or ''
				duration, plot, genre, trailer = self.meta_get('duration'), self.meta_get('plot'), self.meta_get('genre'), self.meta_get('trailer')
				rating, votes, premiered, studio = self.meta_get('rating'), self.meta_get('votes'), self.meta_get('premiered'), self.meta_get('studio')
				listitem = make_listitem()
				listitem.setPath(url)
				if self.media_type == 'movie':
					listitem.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id)})
					listitem.setInfo('video', {'mediatype': 'movie', 'trailer': trailer, 'title': self.title, 'size': '0', 'duration': duration, 'plot': plot,
						'rating': rating, 'premiered': premiered, 'studio': studio,'year': self.year, 'genre': genre, 'tagline': self.meta_get('tagline'), 'code': self.imdb_id,
						'imdbnumber': self.imdb_id, 'director': self.meta_get('director'), 'writer': self.meta_get('writer'), 'votes': votes})
				else:
					listitem.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id), 'tvdb': str(self.tvdb_id)})
					listitem.setInfo('video', {'mediatype': 'episode', 'trailer': trailer, 'title': self.meta_get('ep_name'), 'imdbnumber': self.imdb_id,
						'tvshowtitle': self.title, 'size': '0', 'plot': plot, 'year': self.year, 'votes': votes, 'premiered': premiered, 'studio': studio, 'genre': genre,
						'season': self.season, 'episode': self.episode, 'duration': duration, 'rating': rating, 'FileNameAndPath': url})
				listitem.setCast(self.meta_get('cast', []))
				if get_fanart_data():
					banner, clearart, landscape = self.meta_get('banner'), self.meta_get('clearart'), self.meta_get('landscape')
				else: banner, clearart, landscape = '', '', ''
				listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape,
								'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': landscape, 'tvshow.banner': banner})
				listitem.setProperty('StartPercent', str(bookmark))
				if self.disable_content_lookup: listitem.setContentLookup(False)
				try:
					clear_property('script.trakt.ids')
					trakt_ids = {'tmdb': self.tmdb_id, 'imdb': self.imdb_id, 'slug': make_trakt_slug(self.title)}
					if self.media_type == 'episode': trakt_ids['tvdb'] = self.tvdb_id
					set_property('script.trakt.ids', json.dumps(trakt_ids))
				except: pass
			except: pass
			self.play(url, listitem)
			self.monitor()
		except:
			try: self.object.playback_successful = True
			except: pass

	def bookmark(self):
		percent = get_progress_percent(get_bookmarks(watched_indicators(), self.media_type), self.tmdb_id, self.season, self.episode)
		if percent:
			bookmark = self.getResumeStatus(percent)
			if bookmark == 0: erase_bookmark(self.media_type, self.tmdb_id, self.season, self.episode)
		else: bookmark = 0
		return bookmark

	def getResumeStatus(self, percent):
		if auto_resume(self.media_type): return percent
		choice = confirm_progress_media(meta=self.meta, text=ls(32790) % percent, enable_buttons=True, true_button=32832, false_button=32833, focus_button=10, percent=percent)
		return percent if choice == True else 0 if choice == False else 'cancel'

	def monitor(self):
		if self.media_type == 'episode':
			self.play_random_continual = 'random_continual' in self.meta
			play_random = 'random' in self.meta
			disable_autoplay_next_episode = 'disable_autoplay_next_episode' in self.meta
			if any((self.play_random_continual, play_random, disable_autoplay_next_episode)):
				self.autoplay_next_episode = False
				if disable_autoplay_next_episode: notification('%s - %s %s' % (ls(32135), ls(32178), ls(32736)), 6000)
			else: self.autoplay_next_episode = autoplay_next_episode()
		self.check_playback_start()
		if self.failed_playback:
			try: self.object.playback_successful = self.return_value
			except: pass
			return
		else:
			try: self.object.playback_successful = True
			except: pass
		sleep(1000)
		while self.isPlayingVideo():
			try:
				sleep(1000)
				self.total_time, self.curr_time = self.getTotalTime(), self.getTime()
				self.current_point = round(float(self.curr_time/self.total_time * 100), 1)
				if self.current_point >= self.set_watched and not self.media_marked:
					self.media_watched_marker()
					if self.play_random_continual: self.run_random_continual()
				if self.autoplay_next_episode:
					if not self.nextep_info_gathered: self.info_next_ep()
					self.remaining_time = round(self.total_time - self.curr_time)
					if self.remaining_time <= self.start_prep:
						if not self.nextep_started: self.run_next_ep()
			except: pass
			if not self.subs_searched: self.run_subtitles()
		if not self.media_marked: self.media_watched_marker()
		clear_local_bookmarks()
		sys.exit()

	def media_watched_marker(self):
		self.media_marked = True
		try:
			if self.current_point >= self.set_watched:
				if self.media_type == 'movie':
					watched_function = mark_as_watched_unwatched_movie
					watched_params = {'action': 'mark_as_watched', 'tmdb_id': self.tmdb_id, 'title': self.title, 'year': self.year, 'refresh': 'false', 'from_playback': 'true'}
				else:
					watched_function = mark_as_watched_unwatched_episode
					watched_params = {'action': 'mark_as_watched', 'season': self.season, 'episode': self.episode, 'tmdb_id': self.tmdb_id,
									'title': self.title, 'year': self.year, 'tvdb_id': self.tvdb_id, 'refresh': 'false', 'from_playback': 'true'}
				Thread(target=self.run_media_progress, args=(watched_function, watched_params)).start()
			else:
				clear_property('david_nextep_autoplays')
				clear_property('david_random_episode_history')
				if self.current_point >= self.set_resume:
					progress_params = {'media_type': self.media_type, 'tmdb_id': self.tmdb_id, 'curr_time': self.curr_time,
									'total_time': self.total_time, 'title': self.title, 'season': self.season, 'episode': self.episode}
					Thread(target=self.run_media_progress, args=(set_bookmark, progress_params)).start()
		except: pass

	def run_media_progress(self, function, params):
		try: function(params)
		except: pass

	def run_next_ep(self):
		self.nextep_started = True
		try:
			from modules.episode_tools import execute_nextep
			Thread(target=execute_nextep, args=(self.meta, self.nextep_settings)).start()
		except: pass

	def run_random_continual(self):
		try:
			from modules.episode_tools import play_random_continual
			Thread(target=play_random_continual, args=(self.tmdb_id,)).start()
		except: pass

	def check_playback_start(self):
		count = 0
		while not self.isPlayingVideo():
			sleep(100)
			count += 1
			if get_visibility('Window.IsTopMost(okdialog)'): return self.set_failed_playback(clear_dialog=True)
			if count == self.max_count: return self.set_failed_playback()
	
	def set_failed_playback(self, clear_dialog=False):
		if clear_dialog: execute_builtin("SendClick(okdialog, 11)")
		else: self.stop()
		sleep(1000)
		self.failed_playback = True
		if self.check_successful_playback: self.return_value = False
		else: self.return_value = True

	def run_subtitles(self):
		self.subs_searched = True
		try:
			season = self.season if self.media_type == 'episode' else None
			episode = self.episode if self.media_type == 'episode' else None
			Thread(target=Subtitles().get, args=(self.title, self.imdb_id, season, episode)).start()
		except: pass

	def info_next_ep(self):
		self.nextep_info_gathered = True
		try:
			self.nextep_settings = autoplay_next_settings()
			if self.nextep_settings['run_popup']:
				percentage = self.nextep_settings['window_percentage']
				window_time = round((percentage/100) * self.total_time)
				self.nextep_settings['window_time'] = window_time
			else:
				window_time = round(0.02 * self.total_time)
				self.nextep_settings['window_time'] = window_time
			threshold_check = window_time + 21
			self.start_prep = self.nextep_settings['scraper_time'] + threshold_check
			self.nextep_settings.update({'threshold_check': threshold_check, 'start_prep': self.start_prep})
		except: pass

class Subtitles(xbmc_player):
	def __init__(self):
		xbmc_player.__init__(self)
		self.os = OpenSubtitlesAPI()
		self.language_dict = language_choices
		self.auto_enable = get_setting('subtitles.auto_enable')
		self.subs_action = get_setting('subtitles.subs_action')
		self.language = self.language_dict[get_setting('subtitles.language')]
		self.quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webdl', 'webrip', 'webcap', 'web', 'hdtv', 'hdrip']

	def get(self, query, imdb_id, season, episode):
		def _notification(line, _time=3500):
			return notification(line, _time)
		def _video_file_subs():
			try: available_sub_language = self.getSubtitles()
			except: available_sub_language = ''
			if available_sub_language == self.language:
				if self.auto_enable == 'true': self.showSubtitles(True)
				_notification(32852)
				return True
			return False
		def _downloaded_subs():
			files = list_dirs(subtitle_path)[1]
			if len(files) > 0:
				match_lang1 = None
				match_lang2 = None
				files = [i for i in files if i.endswith('.srt')]
				for item in files:
					if item == search_filename:
						match_lang1 = item
						break
				final_match = match_lang1 if match_lang1 else match_lang2 if match_lang2 else None
				if final_match:
					subtitle = os.path.join(subtitle_path, final_match)
					_notification(32792)
					return subtitle
			return False
		def _searched_subs():
			chosen_sub = None
			result = self.os.search(query, imdb_id, self.language, season, episode)
			if not result or len(result) == 0:
				_notification(32793)
				return False
			try: video_path = self.getPlayingFile()
			except: video_path = ''
			if '|' in video_path: video_path = video_path.split('|')[0]
			video_path = os.path.basename(video_path)
			if self.subs_action == '1':
				self.pause()
				choices = [i for i in result if i['SubLanguageID'] == self.language and i['SubSumCD'] == '1']
				if len(choices) == 0:
					_notification(32793)
					return False
				dialog_list = ['[B]%s[/B] | [I]%s[/I]' % (i['SubLanguageID'].upper(), i['MovieReleaseName']) for i in choices]
				list_items = [{'line1': item} for item in dialog_list]
				kwargs = {'items': json.dumps(list_items), 'heading': video_path.replace('%20', ' '), 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
				chosen_sub = select_dialog(choices, **kwargs)
				self.pause()
				if not chosen_sub:
					_notification(32736, _time=1500)
					return False
			else:
				try: chosen_sub = [i for i in result if i['MovieReleaseName'].lower() in video_path.lower() and i['SubLanguageID'] == self.language and i['SubSumCD'] == '1'][0]
				except: pass
				if not chosen_sub:
					fmt = re.split(r'\.|\(|\)|\[|\]|\s|\-', video_path)
					fmt = [i.lower() for i in fmt]
					fmt = [i for i in fmt if i in self.quality]
					if season and fmt == '': fmt = 'hdtv'
					result = [i for i in result if i['SubSumCD'] == '1']
					filter = [i for i in result if i['SubLanguageID'] == self.language \
												and any(x in i['MovieReleaseName'].lower() for x in fmt) and any(x in i['MovieReleaseName'].lower() for x in self.quality)]
					filter += [i for i in result if any(x in i['MovieReleaseName'].lower() for x in self.quality)]
					filter += [i for i in result if i['SubLanguageID'] == self.language]
					if len(filter) > 0: chosen_sub = filter[0]
					else: chosen_sub = result[0]
			try: lang = convert_language(chosen_sub['SubLanguageID'])
			except: lang = chosen_sub['SubLanguageID']
			sub_format = chosen_sub['SubFormat']
			final_filename = sub_filename + '_%s.%s' % (lang, sub_format)
			download_url = chosen_sub['ZipDownloadLink']
			temp_zip = os.path.join(subtitle_path, 'temp.zip')
			temp_path = os.path.join(subtitle_path, chosen_sub['SubFileName'])
			final_path = os.path.join(subtitle_path, final_filename)
			subtitle = self.os.download(download_url, subtitle_path, temp_zip, temp_path, final_path)
			sleep(1000)
			return subtitle
		if self.subs_action == '2': return
		sleep(2500)
		imdb_id = re.sub(r'[^0-9]', '', imdb_id)
		subtitle_path = translate_path('special://temp/')
		sub_filename = 'DAVIDSubs_%s_%s_%s' % (imdb_id, season, episode) if season else 'DAVIDSubs_%s' % imdb_id
		search_filename = sub_filename + '_%s.srt' % self.language
		subtitle = _video_file_subs()
		if subtitle: return
		subtitle = _downloaded_subs()
		if subtitle: return self.setSubtitles(subtitle)
		subtitle = _searched_subs()
		if subtitle: return self.setSubtitles(subtitle)





