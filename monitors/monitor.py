import requests
import threading
from bs4 import BeautifulSoup as bsoup
from requests_futures.sessions import FuturesSession
class monitor:
	def __init__(self):
		self.needs_soup

	def refresh(self):
		pass

	def check_stock(self):
		raise NotImplementedError("check_stock must be defined in child monitor class.")

	def scrape(self):
		n = len(self.links)
		if n < 0:
			n = 1
		session = FuturesSession(max_workers=n)
		reqs = (session.get(link) for link in self.links)
		self.responses = [r.result() for r in reqs]
		# print(self.responses)
		self.soups = []
		if self.needs_soup:
			for resp in self.responses:
				self.soups.append(self.make_soup(resp))
			
	def make_soup(self, response):
		return bsoup(response.content, 'html.parser')

	def run(self):
		print(self.url)
		self.refresh()
		print(len(self.links))
		self.scrape()
		threads = []
		for i in range(len(self.links)):
			t = threading.Thread(target=self.check_stock, args=(i,))
			t.start()
			threads.append(t)
		for t in threads:
			t.join()

class soup:
	def __init__(self, link):
		self.response = requests.get(link)
		self.soup = bsoup(self.response.content, 'html.parser')

class request:
	def __init__(self, link):
		self.response = requests.get(link)