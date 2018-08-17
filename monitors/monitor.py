import requests
import threading
import time
from frostcop.utils import discord_utils
from bs4 import BeautifulSoup as bsoup
from requests_futures.sessions import FuturesSession
class monitor:
	needs_soup = False
	ctime = 0
	def __init__(self):
		pass

	def refresh(self):
		"""
		If a monitor has a list of links it must check,
		it overrides the refresh function. This is not
		required, so it is implemented here as an empty
		method to prevent errors.
		"""
		pass

	def check(self):
		"""
		All monitors must have a method to check the
		stock of their items. If a monitor class does
		not override this method, an error is thrown.
		"""
		raise NotImplementedError("check must be defined in child monitor class.")

	def scrape(self):
		n = len(self.links)
		if n < 0:
			n = 1
		session = FuturesSession(max_workers=n)
		reqs = ()
		for link in self.links:
			reqs += (session.get(link),)
		self.responses = [r.result() for r in reqs]
		print(self.responses)
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
		"""
		Returns an HTTP GET request for the specified
		web address, and throws an error after a
		timeout of 5 seconds.
		"""
		return requests.get(link, timeout=5)
			
	def soupify(self, response):
		"""
		Uses BeautifulSoup4 to return the HTML content
		of the specified HTTP response, as obtained
		using the requests module. "response" is not
		a web address, but an already pinged response
		object generated from an address.
		"""
		print('souping')
		return bsoup(response.content, 'html.parser')

	def run(self):
		self.ctime = time.time()
		self.refresh()
		quit()
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