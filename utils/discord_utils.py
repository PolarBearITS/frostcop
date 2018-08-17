import requests
from datetime import datetime
class Webhook:
	def __init__(self, url, **kwargs):
		self.url = url
		self.data = {}
		self.kw_names = {
			'content': str,
			'username': str,
			'avatar_url': str,
			'tts': bool,
			'file': bytes,
			'embeds': list,
		}
		for n, t in self.kw_names.items():
			if n in kwargs:
				try:
					v = kwargs.get(n)
					assert isinstance(v, t)
					self.data[n] = v
				except AssertionError as e:
					raise Exception(f'Param "{n}"" was of type {type(v).__name__}, but must be of type {t.__name__}.') from e
		if 'embeds' in self.__dict__:
			if any(not isinstance(l, Embed) for l in self.embeds):
				raise Exception(f'Param "embeds" must only contain Embed objects')
	def post(self):
		r = requests.post(self.url, json=self.data)
		print(r, requests.status_codes._codes[r.status_code], r.content)

class Embed:
	def __init__(self, **kwargs):
		self.kw_names = {
			'title': str,
			'type': str,
			'description': str,
			'url': str,
			'timestamp': str,
			'color': int,
			'footer': Footer,
			'image': Image,
			'thumbnail': dict,
			'video': dict,
			'provider': dict,
			'author': dict,
			'fields': dict,
		}

	class Footer:
		def __init__(self, **kwargs):
			self.kw_names = {
				'text': str,
				'icon_url': str,
				'proxy_icon_url': str,
			}
	class Image:
		def __init__(self, **kwargs):
			self.kw_names = {
				'url': str,
				'proxy_url': str,
				'height': int,
				'width': int,
			}
