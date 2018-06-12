import requests
import threading
import time
from bs4 import BeautifulSoup as bsoup
from requests_futures.sessions import FuturesSession
class monitor:
	needs_soup = False
	ctime = 0
	def __init__(self):
		pass

	def refresh(self):
		pass

	def check_stock(self):
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

	def request(self, link):
		return requests.get(link, timeout=5)
			
	def soupify(self, response):
		return bsoup(response.content, 'html.parser')

	def run(self):
		self.ctime = time.time()
		self.refresh()
		print('refresh done')
		self.scrape()
		print('scrape done')
		threads = []
		for i in range(len(self.links)):
			t = threading.Thread(target=self.check_stock, args=(i,))
			t.start()
			threads.append(t)
		for t in threads:
			t.join()
		print(len(self.links), time.time()-self.ctime)

class product:
	def __init__(self, uid, name, price, stock, **kwargs):
		self.uid = uid
		self.name = name
		self.stock = stock
		kw_names = ['variant', 'sizes']
		for name in kw_names:
			if name in kwargs:
				setattr(self, name, kwargs.get(name))
		print(self.__dict__)