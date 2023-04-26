# -*- coding: utf-8 -*-
from windows import BaseDialog
from modules.settings import get_art_provider, get_fanart_data
from modules.kodi_utils import empty_poster, addon_fanart, get_setting
# from modules.kodi_utils import logger

class ConfirmProgressMedia(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.is_canceled = False
		self.selected = None
		self.meta = kwargs['meta']
		self.text = kwargs.get('text', '')
		self.enable_buttons = kwargs.get('enable_buttons', False)
		self.fanart_background = 'false' if self.enable_buttons else get_setting('results.fanart_background')
		self.true_button = kwargs.get('true_button', '')
		self.false_button = kwargs.get('false_button', '')
		self.focus_button = kwargs.get('focus_button', 10)
		self.percent = float(kwargs.get('percent', 0))
		self.make_items()
		self.set_properties()

	def onInit(self):
		if self.enable_buttons: self.allow_buttons()

	def run(self):
		self.doModal()
		self.clearProperties()
		return self.selected

	def iscanceled(self):
		if self.enable_buttons: return self.selected
		else: return self.is_canceled

	def onAction(self, action):
		if action in self.closing_actions:
			self.is_canceled = True
			self.close()

	def onClick(self, controlID):
		self.selected = controlID == 10
		self.close()

	def allow_buttons(self):
		self.setProperty('source_progress.buttons', 'true')
		self.setProperty('source_progress.true_button', self.true_button)
		self.setProperty('source_progress.false_button', self.false_button)
		self.update(self.text, self.percent)
		self.setFocusId(self.focus_button)

	def make_items(self):
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup, self.clearlogo_main, self.clearlogo_backup = get_art_provider()
		self.title = self.meta['title']
		self.year = str(self.meta['year'])
		self.poster = self.meta.get(self.poster_main) or self.meta.get(self.poster_backup) or empty_poster
		self.fanart = self.meta.get(self.fanart_main) or self.meta.get(self.fanart_backup) or addon_fanart
		self.clearlogo = self.meta.get(self.clearlogo_main) or self.meta.get(self.clearlogo_backup) or ''

	def set_properties(self):
		self.setProperty('source_progress.title', self.title)
		self.setProperty('source_progress.year', self.year)
		self.setProperty('source_progress.poster', self.poster)
		self.setProperty('source_progress.fanart', self.fanart)
		self.setProperty('source_progress.clearlogo', self.clearlogo)
		self.setProperty('source_progress.fanart_background', self.fanart_background)

	def update(self, content='', percent=0):
		try:
			self.getControl(2000).setText(content)
			self.getControl(5000).setPercent(percent)
		except: pass
