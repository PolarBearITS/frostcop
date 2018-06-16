import requests
import threading
import time
from . import discord_utils
from bs4 import BeautifulSoup as bsoup
from requests_futures.sessions import FuturesSession
class monitor:
	needs_soup = False
	ctime = 0
	def __init__(self):
		pass

	def refresh(self):
		pass

	def check(self):
		raise NotImplementedError("check_stock must be defined in child monitor class.")

	def scrape(self):
		n = len(self.links)
		if n < 0:
			n = 1
		session = FuturesSession(max_workers=n)
		reqs = ()
		for link in self.links:
			reqs += (session.get(link),)
		self.responses = [r.result() for r in reqs]
		self.soups = []
		if self.needs_soup:
			for resp in self.responses:
				self.soups.append(self.soupify(resp))

	def update(self, product):
		if not hasattr(self, 'stock'):
			self.stock = {}
			self.initialized = False
		if self.initialized:
			if product.uid not in self.stock:
				self.notify(product, 'new')
			elif product.stock != self.stock[product.uid].stock:
				self.notify(product, 'restock')
		self.stock[product.uid] = product

	def notify(self, product, notification_type):
		print(self.webhook, repr(product), notification_type)

	def request(self, link):
		return requests.get(link, timeout=5)
			
	def soupify(self, response):
		return bsoup(response.content, 'html.parser')

	def run(self):
		self.ctime = time.time()
		self.refresh()
		self.scrape()
		threads = []
		for i in range(len(self.links)):
			t = threading.Thread(target=self.check, args=(i,))
			t.daemon = True
			t.start()
			threads.append(t)
		for t in threads:
			t.join()
		if not self.initialized:
			self.initialized = True
		print(self.__class__.__name__, len(threads), round(time.time()-self.ctime, 7))

class product:
	def __init__(self, uid, name, price, stock, **kwargs):
		self.uid = uid
		self.name = name
		self.stock = stock
		kw_names = ['variant', 'sizes']
		for name in kw_names:
			if name in kwargs:
				setattr(self, name, kwargs.get(name))
	def __str__(self):
		return str(self.__dict__)